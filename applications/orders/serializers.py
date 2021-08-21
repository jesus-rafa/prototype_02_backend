from applications.users.models import User
from django.db.models import fields
from rest_framework import pagination, serializers

from .models import Order, OrderItem


class UsersSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'get_full_name',
            'get_initials',
            'avatar'
        )


class CRUD_OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            "id",
            "order",
            "product",
            "description",
            "price",
            "quantity",
        )


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            "id",
            "product",
            "description",
            "price",
            "quantity",
        )


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user = UsersSerializers()

    class Meta:
        model = Order
        fields = (
            'id',
            'event',
            'user',
            'date',
            'amount',
            'amount_paid',
            'quantity',
            'paid_out',
            'tip',
            'remaining',
            'items'
        )


class PaidOutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = (
            'amount_paid',
        )


class PaginationSerializer(pagination.PageNumberPagination):

    page_size = 10
    max_page_size = 50
