# django
from django.urls import include, path, re_path

# local
from . import views

app_name = "orders_app"

urlpatterns = [
    # lista orden por evento
    path(
        'api/orders/by-event/<id>/',
        views.List_OrderEvent.as_view(),
    ),
    # lista orden por evento y por usuario
    path(
        'api/orders/by-user/<int:idEvent>/<int:idUser>',
        views.List_OrderUser.as_view(),
    ),
    # Agregar productos al carrito
    path(
        'api/orders/cart/add/',
        views.AddCart.as_view(),
    ),
    # Agregar productos al carrito
    path(
        'api/orders/cart/edit/<int:pk>/',
        views.EditCart.as_view(),
    ),
    # Eliminar productos del carrito
    path(
        'api/orders/cart/remove/<int:pk>/',
        views.RemoveCart.as_view(),
    )
]
