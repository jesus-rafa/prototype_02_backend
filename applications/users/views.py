# from django.contrib.sites.models import Site
import datetime
import os
import random
import string
from email.mime.image import MIMEImage

from applications.events.models import Event, Participants
from applications.orders.models import Order
from applications.users import serializers
from applications.users.models import Membership, Tribes, User
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.core.mail import (EmailMessage, EmailMultiAlternatives, send_mail,
                              send_mass_mail)
from django.db.models import query
from django.shortcuts import redirect, render
from django.template import Context
from django.template.loader import get_template, render_to_string
from django.views.generic import TemplateView, View
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (AdminSerializer, ChangePasswordSerializer,
                          ContactSerializer, CRUD_TribesSerializer,
                          EmailSerializer, InvitationSerializer,
                          ListAdminSerializer, ListMembersSerializer,
                          LoginSerializer, MembersSerializer,
                          RegisterSerializer, RetrieveMembersSerializer,
                          TribesSerializer, UserSerializer)


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LeaveTribe(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):

        idGroup = self.kwargs['pk']
        idUser = self.kwargs['idUser']

        instance = Tribes.objects.get(pk=idGroup, members=idUser)
        instance.members.remove(idUser)
        instance.save()

        return Response({
            "response": 'ok'
        })


class UserAPI(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class EditUserAPI(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = UserSerializer
    queryset = User.objects.all()


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Contraseña Actual es Incorrecta."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Contraseña Actualizada',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendEmail(TemplateView):
    # template_name = 'users/reset_email.html'
    template_name = 'payments/mercadopago.html'


class SendFormEmail(View):

    def get(self, request):

        # Get the form data
        name = request.GET.get('name', None)
        email = request.GET.get('email', None)
        message = request.GET.get('message', None)

        # Send Email
        send_mail(
            'Invitacion a un evento',
            'Hello ' + name + ',\n' + message,
            'rafalopezrl749@gmail.com',  # Admin
            [
                email,
            ]
        )

        # Redirect to same page after form submit
        messages.success(request, ('Email sent successfully.'))
        return True


class Delivered(CreateAPIView):
    """ Enviar correos a todos los miembros de la tribu """
    serializer_class = InvitationSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request,  *args, **kwargs):
        serializer = InvitationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Recuperar datos
        idEvent = serializer.validated_data['idEvent']
        listEmails = serializer.validated_data['listEmails']
        # listRegisteredEmails = []

        event = Event.objects.filter(id=idEvent)
        # event_instance = Event.objects.get(id=idEvent)
        # event_instance.status = 'EN PROCESO'
        # event_instance.save()

        # cargar adjuntos en el email
        if event[0].image:
            coupon_image = event[0].image
            img_data = coupon_image.read()
            img = MIMEImage(img_data)
            img.add_header('Content-ID', '<coupon_image>')

        # Envio de correos para usuarios ya registrados
        subject = 'Invitacion a un Evento: ' + event[0].name
        text_content = ''
        html_content = render_to_string(
            'users/email/delivered.html',
            {'data': event}
        )
        msg = EmailMultiAlternatives(
            subject,
            text_content,
            settings.EMAIL_HOST_USER,
            listEmails
        )
        msg.attach_alternative(html_content, "text/html")
        if event[0].image:
            msg.mixed_subtype = 'related'
            msg.attach(img)
        msg.send()

        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Pedido Entregado Exitosamente!'
        }

        return Response(response)


class Thank(CreateAPIView):
    def create(self, request,  *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Recuperar datos
        listEmails = serializer.validated_data['listEmails']
        print('-----------------------------------------------------')
        print(request.data)
        print('-----------------------------------------------------')
        # Envio de correos para usuarios ya registrados
        subject = 'Invitacion a un Evento: '
        text_content = ''
        html_content = render_to_string(
            'users/email/thank.html',
            {'data': listEmails}
        )
        msg = EmailMultiAlternatives(
            subject,
            text_content,
            settings.EMAIL_HOST_USER,
            listEmails
        )
        msg.attach_alternative(html_content, "text/html")
        msg.mixed_subtype = 'related'
        msg.send()

        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Pedido Entregado Exitosamente!'
        }

        return Response(response)


class Invitations(CreateAPIView):
    """ Enviar correos a todos los miembros de la tribu """
    serializer_class = InvitationSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request,  *args, **kwargs):
        serializer = InvitationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Recuperar datos
        idEvent = serializer.validated_data['idEvent']
        listEmails = serializer.validated_data['listEmails']
        listRegisteredEmails = []

        # Recuperar instancia del evento
        event = Event.objects.filter(id=idEvent)
        event_instance = Event.objects.get(id=idEvent)
        event_instance.status = 'EN PROCESO'
        event_instance.save()

        # cargar adjuntos en el email
        if event[0].image:
            coupon_image = event[0].image
            img_data = coupon_image.read()
            img = MIMEImage(img_data)
            img.add_header('Content-ID', '<coupon_image>')

        for email in listEmails:
            if User.objects.filter(email=email).exists():
                user_instance = User.objects.get(email=email)
            else:
                user_instance = None

            # Crear las ordenes de cada participante
            if user_instance:
                # Order.objects.create(
                #     event=event_instance,
                #     user=user_instance,
                #     date=datetime.date.today()
                # )

                listRegisteredEmails.append(email)
            else:
                # Si el correo no esta registrado lo inserta
                password = ''.join(
                    [random.choice(string.digits + string.ascii_letters)
                     for i in range(0, 8)]
                )

                User.objects.create_user(
                    email, password, '', ''
                )
                # user_new = User.objects.get(email=email)

                # Order.objects.create(
                #     event=event_instance,
                #     user=user_new,
                #     date=datetime.date.today()
                # )

                # Envio de correos para usuarios nuevos
                subject = 'Invitacion a un Evento: ' + event[0].name
                text_content = ''
                html_content = render_to_string(
                    'users/email/card_new.html',
                    {'data': event, 'email': email, 'password': password}
                )
                msg2 = EmailMultiAlternatives(
                    subject,
                    text_content,
                    settings.EMAIL_HOST_USER,
                    [email]
                )
                msg2.attach_alternative(html_content, "text/html")
                if event[0].image:
                    msg2.mixed_subtype = 'related'
                    msg2.attach(img)
                msg2.send()

        # Envio de correos para usuarios ya registrados
        subject = 'Invitacion a un Evento: ' + event[0].name
        text_content = ''
        html_content = render_to_string(
            'users/email/card.html',
            {'data': event}
        )
        msg = EmailMultiAlternatives(
            subject,
            text_content,
            settings.EMAIL_HOST_USER,
            listRegisteredEmails
        )
        msg.attach_alternative(html_content, "text/html")
        if event[0].image:
            msg.mixed_subtype = 'related'
            msg.attach(img)
        msg.send()

        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Invitaciones Enviadas Exitosamente!'
        }

        return Response(response)


class ListUsers(ListAPIView):
    """
        Lista todos los usuarios mortales
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = MembersSerializer

    def get_queryset(self):

        # return User.objects.filter(is_superuser=False)
        return User.objects.all()


class List_Tribes(ListAPIView):
    """
        Lista los grupos creados por cada usuario
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = TribesSerializer

    def get_queryset(self):
        # idUser = self.kwargs['id']
        idUser = self.request.user.id

        return Tribes.objects.tribes_by_user(idUser)


class List_BelongTribes(ListAPIView):
    """
        Lista los grupos a los que pertenece cada usuario
    """
    # permission_classes = (IsAuthenticated,)
    serializer_class = TribesSerializer

    def get_queryset(self):
        # idUser = self.kwargs['id']
        idUser = self.request.user.id

        return Tribes.objects.belong_to_tribes(idUser)


class List_Users(ListAPIView):
    """
        Vista para listar grupos por usuario
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = MembersSerializer

    def get_queryset(self):
        kword = self.request.query_params.get('kword', '')

        if kword != '':
            queryset = User.objects.filter(
                names__icontains=kword
            )
        else:
            queryset = []
        return queryset


class List_Groups(ListAPIView):
    """
        Vista para listar grupos
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = TribesSerializer

    def get_queryset(self):
        kword = self.request.query_params.get('kword', '')

        if kword != '':
            queryset = Tribes.objects.filter(
                name__icontains=kword
            )
        else:
            queryset = []
        return queryset


class RetrieveMemebers(ListAPIView):
    """
        Devuelve los miembros de cada tribu
    """
    # permission_classes = (IsAuthenticated,)
    serializer_class = RetrieveMembersSerializer

    def get_queryset(self):
        idTribe = self.kwargs['pk']

        return Tribes.objects.filter(
            pk=idTribe
        )


class AddTribes(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CRUD_TribesSerializer

    def post(self, request, *args, **kwargs):
        serializer = CRUD_TribesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Recuperamos datos
        members = serializer.validated_data['members']
        name = serializer.validated_data['name']
        idUser = serializer.validated_data['user']

        if Tribes.objects.filter(name=name).exists():
            return Response({"error": "Ya existe este grupo: " + name}, status=status.HTTP_400_BAD_REQUEST)
        else:

            try:
                description = serializer.validated_data['description']
            except:
                description = ''

            try:
                avatar = serializer.validated_data['avatar']
            except:
                avatar = None

            # Instancia del user
            instance_user = User.objects.get(id=idUser)

            # Se crea el grupo
            instance_group = Tribes.objects.create(
                name=name,
                description=description,
                user=instance_user,
                avatar=avatar,
            )

            # Agregar miembros a la lista: list_members[]
            list_members = []
            for member in members:
                instance_member = User.objects.get(id=member)
                members = Membership(
                    group=instance_group,
                    user=instance_member,
                    is_admin=False
                )
                list_members.append(members)

            # Insertamos list_members[]
            Membership.objects.bulk_create(list_members)

            success = "Grupo creado exitosamente!"

            return Response({'success': success})


class EditTribes(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = CRUD_TribesSerializer
    queryset = Tribes.objects.all()

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        # Recuperamos datos
        name = serializer.validated_data['name']
        members = serializer.validated_data['members']

        if instance.name != name:
            if Tribes.objects.filter(name=name).exists():
                return Response({"error": "Ya existe este grupo: " + name}, status=status.HTTP_400_BAD_REQUEST)

            # guardarmos nuevo nombre del grupo
            instance.name = name

        try:
            description = serializer.validated_data['description']
        except:
            description = ''

        try:
            avatar = serializer.validated_data['avatar']
        except:
            avatar = None

        if description != '':
            instance.description = description

        if avatar != None:
            instance.avatar = avatar

        # Filtrar usuarios actuales
        data = Membership.objects.filter(group=instance)

        for row in data:
            instance_member = User.objects.get(email=row.user)

            # eliminar usuarios del grupo
            if not str(instance_member.id) in members:
                instance.members.remove(instance_member)

        new_members = []
        for row in members:
            instance_member = User.objects.get(id=row)

            # Buscamos si el usuario ya existe en el grupo
            member = Membership.objects.filter(
                group=instance,
                user=str(row)
            )

            # Agregar miembros a la lista: new_members[]
            if not member:
                members = Membership(
                    group=instance,
                    user=instance_member,
                    is_admin=False
                )
                new_members.append(members)

        # Insertamos los nuevos usuarios new_members[]
        Membership.objects.bulk_create(new_members)

        # Guardamos instancia
        instance.save()

        success = "Grupo actualizado exitosamente!"

        return Response({'success': success})


class AssignPermissions(UpdateAPIView):
    # permission_classes = (IsAuthenticated,)

    serializer_class = AdminSerializer
    queryset = Tribes.objects.all()

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        # Recuperamos lista de id´s is_admin = True
        members = serializer.validated_data['members']

        # Agregar permisos de admin
        Membership.objects.filter(
            group=instance,
            user__in=members
        ).update(is_admin=True)

        # Quitar permisos de admin
        Membership.objects.filter(
            group=instance
        ).exclude(
            user__in=members
        ).update(is_admin=False)

        return Response({'response': 'ok'})


class RemoveTribes(DestroyAPIView):
    permission_classes = [IsAuthenticated, ]

    serializer_class = CRUD_TribesSerializer
    queryset = Tribes.objects.all()


class Contact(generics.GenericAPIView):
    serializer_class = ContactSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        contact = serializer.validated_data['contact']
        email = serializer.validated_data['email']
        message = serializer.validated_data['message']

        # Envio de correo
        subject = 'Contacto: ' + contact
        text_content = ''
        html_content = render_to_string(
            'users/email/contact.html',
            {'contact': contact, 'email': email, 'message': message}
        )
        msg = EmailMultiAlternatives(
            subject,
            text_content,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return Response({'response': 'ok'})
