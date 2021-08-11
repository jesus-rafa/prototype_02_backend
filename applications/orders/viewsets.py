from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
#
from .models import Order, OrderItem
#
from .serializers import (
    OrderSerializer,
    PaginationSerializer
)


class OrdersViewSet(viewsets.ModelViewSet):

    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    pagination_class = PaginationSerializer
