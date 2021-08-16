# apps de terceros
from applications.events import serializers
#
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveAPIView, UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

# local models
from .models import Event, Event_Detail
# local serialiozers
from .serializers import (CRUD_DetailEventSerializer, CRUD_EventSerializer,
                          DetailSerializer, EventSerializer,
                          PaginationSerializer)


class List_EventUser(ListAPIView):
    """
        Vista eventos por usuario
    """
    serializer_class = EventSerializer

    def get_queryset(self):
        idUser = self.kwargs['id']

        return Event.objects.events_by_user(idUser)


class List_DetailEvent(ListAPIView):
    """
        Vista eventos por usuario
    """
    serializer_class = CRUD_DetailEventSerializer

    def get_queryset(self):
        idEvent = self.kwargs['id']

        return Event_Detail.objects.filter(name=idEvent)


class CreateDetail(CreateAPIView):
    serializer_class = CRUD_DetailEventSerializer
    queryset = Event_Detail.objects.all()


class UpdateDetail(UpdateAPIView):
    serializer_class = CRUD_DetailEventSerializer
    queryset = Event_Detail.objects.all()


class List_Events(ListAPIView):
    """
        filtrar eventos por Estatus
    """
    serializer_class = EventSerializer
    pagination_class = PaginationSerializer

    def get_queryset(self):
        status = self.kwargs['status']

        return Event.objects.filter_events(status)


class RetrieveEvent(RetrieveAPIView):
    """
        Recuperar evento
    """
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class List_Detail(ListAPIView):
    """
        Vista para listar eventos
    """
    serializer_class = DetailSerializer

    def get_queryset(self):
        return Event_Detail.objects.all()
