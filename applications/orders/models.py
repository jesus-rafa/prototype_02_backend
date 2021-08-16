from applications.events.models import Event
from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel

from .managers import OrderManager


class Order(TimeStampedModel):
    event = models.ForeignKey(
        Event, related_name='order_event', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='order_user', on_delete=models.CASCADE)
    date = models.DateField('Fecha Pedido')
    amount = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True, default=0)
    quantity = models.IntegerField(default=0)
    paid_out = models.BooleanField(default=False)
    tip = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True, default=0)
    remaining = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True, default=0)

    objects = OrderManager()

    class Meta:
        verbose_name = 'Orden'
        verbose_name_plural = 'Orden'

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    product = models.CharField(
        'Producto',
        max_length=100,
    )
    description = models.CharField(
        'Descripcion',
        max_length=254,
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return '%s' % self.id
