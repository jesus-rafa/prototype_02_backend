#from django.contrib.sites.models import Site
import datetime
import os
import random
import string
from email.mime.image import MIMEImage

from applications.events.models import Event
from applications.orders.models import Order
from applications.users import serializers
from applications.users.models import Tribes, User
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

from .serializers import (ChangePasswordSerializer, CRUD_TribesSerializer,
                          InvitationSerializer, LoginSerializer,
                          MembersSerializer, RegisterSerializer,
                          RetrieveMembersSerializer, TribesSerializer,
                          UserSerializer)


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
    #template_name = 'users/reset_email.html'
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


class Invitations(CreateAPIView):
    """ Enviar correos a todos los miembros de la tribu """
    serializer_class = InvitationSerializer
    #permission_classes = (IsAuthenticated,)

    def create(self, request,  *args, **kwargs):
        serializer = InvitationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Recuperar datos
        idEvent = serializer.validated_data['idEvent']
        listEmails = serializer.validated_data['listEmails']

        #listEmails = ['rafalopezrl749@gmail.com', 'kathia@gmail.com']

        event = Event.objects.filter(id=idEvent)
        event_instance = Event.objects.get(id=idEvent)
        event_instance.status = 'EN PROCESO'
        event_instance.save()

        for email in listEmails:
            user_instance = User.objects.get(email=email)

            # Crear las ordenes de cada participante
            if user_instance:
                Order.objects.create(
                    event=event_instance,
                    user=user_instance,
                    date=datetime.date.today()
                )
            else:
                password = ''.join(
                    [random.choice(string.digits + string.ascii_letters)
                     for i in range(0, 8)]
                )

                User.objects.create_user(
                    email,
                    password,
                    '',
                    '',
                    ''
                )
                user_new = User.objects.get(email=email)

                Order.objects.create(
                    event=event_instance,
                    user=user_new,
                    date=datetime.date.today()
                )

                # Enviar correo de confirmacion
                subject = 'Activar Cuenta'
                text_content = ''
                html_content = render_to_string(
                    'users/email/confirm_account.html',
                    {'email': email, 'password': password}
                )
                msg = EmailMultiAlternatives(
                    subject,
                    text_content,
                    settings.EMAIL_HOST_USER,
                    [email]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                # Enviar correo de confirmacion

        # cargar adjuntos en el email
        coupon_image = event[0].image
        img_data = coupon_image.read()
        img = MIMEImage(img_data)
        img.add_header('Content-ID', '<coupon_image>')

        # Envio de correos
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
            listEmails
        )
        msg.attach_alternative(html_content, "text/html")
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
    serializer_class = MembersSerializer

    def get_queryset(self):

        # return User.objects.filter(is_superuser=False)
        return User.objects.all()


class List_Tribes(ListAPIView):
    """
        Lista los grupos creados por cada usuario
    """
    serializer_class = TribesSerializer

    def get_queryset(self):
        idUser = self.kwargs['id']

        return Tribes.objects.tribes_by_user(idUser)


class List_BelongTribes(ListAPIView):
    """
        Lista los grupos a los que pertenece cada usuario
    """
    serializer_class = TribesSerializer

    def get_queryset(self):
        idUser = self.kwargs['id']

        return Tribes.objects.belong_to_tribes(idUser)


class List_Users(ListAPIView):
    """
        Vista para listar grupos por usuario
    """
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
    serializer_class = RetrieveMembersSerializer

    def get_queryset(self):
        idTribe = self.kwargs['pk']

        return Tribes.objects.filter(
            pk=idTribe
        )


class AddTribes(CreateAPIView):
    # permission_classes = (IsAuthenticated,)

    serializer_class = CRUD_TribesSerializer
    queryset = Tribes.objects.all()

    # def create(self, request, *args, **kwargs):
    #     serializer = CRUD_TribesSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     data = request.data
    #     members = data['members[]'].split(", ")

    #     print(members)

    #     Tribes.objects.create(
    #         name=serializer.validated_data['name'],
    #         description=serializer.validated_data['description'],
    #         user=serializer.validated_data['user'],
    #         avatar=serializer.validated_data['avatar'],
    #         members=members
    #     )

    #     return Response({'res': 'ok'})


class EditTribes(UpdateAPIView):
    # permission_classes = (IsAuthenticated,)

    serializer_class = CRUD_TribesSerializer
    queryset = Tribes.objects.all()


class RemoveTribes(DestroyAPIView):
    # authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    serializer_class = CRUD_TribesSerializer
    queryset = Tribes.objects.all()
