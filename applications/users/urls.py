from django.contrib import admin
from django.urls import path
from knox import views as knox_views

from . import views

app_name = "users_app"

urlpatterns = [
    path(
        'api/register/',
        views.RegisterAPI.as_view(),
    ),
    path(
        'api/login/',
        views.LoginAPI.as_view(),
    ),
    path(
        'api/user/',
        views.UserAPI.as_view(),
    ),
    path(
        'api/users/',
        views.ListUsers.as_view(),
    ),
    path(
        'api/members/',
        views.List_Users.as_view(),
    ),
    path(
        'api/user/edit/<int:pk>/',
        views.EditUserAPI.as_view(),
    ),
    path(
        'api/tribes/assign-permissions/<int:pk>/',
        views.AssignPermissions.as_view(),
    ),
    path(
        'api/change-password/',
        views.ChangePasswordView.as_view(),
    ),
    path(
        'api/reset-password/send-email/',
        views.SendEmail.as_view(),
    ),
    path(
        'api/generate-email/',
        views.SendFormEmail.as_view(),
        name='email'
    ),
    path(
        'api/logout/',
        knox_views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        'api/logoutall/',
        knox_views.LogoutAllView.as_view(),
        name='logoutall'
    ),
    path(
        'api/tribes/by-user/',
        views.List_Tribes.as_view(),
    ),
    path(
        'api/users/belong-tribes/',
        views.List_BelongTribes.as_view(),
    ),
    path(
        'api/tribes/add/',
        views.AddTribes.as_view(),
    ),
    path(
        'api/tribes/edit/<int:pk>/',
        views.EditTribes.as_view(),
    ),
    path(
        'api/tribes/remove/<int:pk>/',
        views.RemoveTribes.as_view(),
    ),
    path(
        'api/tribes/members/<int:pk>/',
        views.RetrieveMemebers.as_view(),
    ),
    path(
        'api/tribes/invitations/',
        views.Invitations.as_view(),
    ),
    path(
        'api/tribes/',
        views.List_Groups.as_view(),
    ),
    # Enviar correo llego pedido
    path(
        'api/tribes/delivered/',
        views.Delivered.as_view(),
    ),
    # Enviar correo agradecimiento
    path(
        'api/tribes/thank/',
        views.Thank.as_view(),
    ),
    path(
        'api/tribes/leave/<int:pk>/<int:idUser>/',
        views.LeaveTribe.as_view(),
    ),
    path(
        'api/users/contact/',
        views.Contact.as_view(),
    ),
]
