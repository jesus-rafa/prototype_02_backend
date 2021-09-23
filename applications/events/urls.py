from django.contrib import admin
from django.urls import path

from . import views

app_name = "events_app"

urlpatterns = [
    # lista eventos
    path(
        'api/events/list/<str:status>/',
        views.List_Events.as_view()
    ),
    # Recuperar evento
    path(
        'api/events/retrieve/<pk>/',
        views.RetrieveEvent.as_view()
    ),
    # Recuperar estatus
    path(
        'api/events/status/<pk>/',
        views.RetrieveStatus.as_view()
    ),
    # Validar que el evento se administre por el creador del mismo
    path(
        'api/events/validate/<pk>/',
        views.ValidateEvent.as_view()
    ),
    # lista detalle de eventos
    path(
        'api/events/detail/<int:id>/',
        views.List_DetailEvent.as_view()
    ),
    # Actualizar estatus del evento
    path(
        'api/events/update-status/<int:pk>/',
        views.UpdateStatus.as_view()
    ),
    # lista eventos por usuario
    path(
        'api/events/by-user/',
        views.List_EventUser.as_view()
    ),
    path(
        'api/events/detail/create/',
        views.CreateDetail.as_view()
    ),
    path(
        'api/events/detail/update/<int:pk>/',
        views.UpdateDetail.as_view(),
    ),

]
