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
    # lista detalle de eventos
    path(
        'api/events/detail/<int:id>/',
        views.List_DetailEvent.as_view()
    ),
    # lista eventos por usuario
    path(
        'api/events/by-user/<int:id>/',
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
