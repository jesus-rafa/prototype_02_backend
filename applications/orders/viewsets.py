from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

#
from .models import Order, OrderItem
#
from .serializers import OrderSerializer, PaginationSerializer


class OrdersViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    pagination_class = PaginationSerializer
