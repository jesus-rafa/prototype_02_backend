# apps de terceros
from applications.events import serializers
from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveAPIView, UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

# local models
from .models import Event, Event_Detail
# local serialiozers
from .serializers import (CRUD_DetailEventSerializer, CRUD_EventSerializer,
                          DetailSerializer, EventSerializer,
                          PaginationSerializer, StatusSerializer)


class List_EventUser(ListAPIView):
    """
        Vista eventos por usuario
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

    def get_queryset(self):
        idUser = self.kwargs['id']

        return Event.objects.events_by_user(idUser)


class List_DetailEvent(ListAPIView):
    """
        Vista eventos por usuario
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = CRUD_DetailEventSerializer

    def get_queryset(self):
        idEvent = self.kwargs['id']

        return Event_Detail.objects.filter(name=idEvent)


class ValidateEvent(generics.GenericAPIView):
    """
        Validar que el evento se administre por el creador del mismo
    """
    #permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):

        idEvent = self.kwargs['pk']
        idUser = self.kwargs['idUser']

        flag = False
        if Event.objects.filter(pk=idEvent, create_by=idUser).exists():
            flag = True

        return Response({'data': flag})


class RetrieveStatus(generics.GenericAPIView):
    """
        Retornar el estatus del evento
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):

        idEvent = self.kwargs['pk']

        query = Event.objects.filter(pk=idEvent)

        return Response({'data': query[0].status})


class CreateDetail(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CRUD_DetailEventSerializer
    queryset = Event_Detail.objects.all()


class UpdateDetail(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CRUD_DetailEventSerializer
    queryset = Event_Detail.objects.all()


class List_Events(ListAPIView):
    """
        filtrar eventos por Estatus
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer
    pagination_class = PaginationSerializer

    def get_queryset(self):
        status = self.kwargs['status']

        return Event.objects.filter_events(status)


class RetrieveEvent(RetrieveAPIView):
    """
        Recuperar evento
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class List_Detail(ListAPIView):
    """
        Vista para listar eventos
    """
    serializer_class = DetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Event_Detail.objects.all()


class UpdateStatus(UpdateAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = StatusSerializer
    queryset = Event.objects.all()

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(
    #         instance, data=request.data, partial=True
    #     )
    #     serializer.is_valid(raise_exception=True)

    #     instance.amount_paid = serializer.validated_data['amount_paid']
    #     if instance.amount >= serializer.validated_data['amount_paid']:
    #         instance.paid_out = True

    #     instance.save()

    #     return Response({'response': 'ok'})
