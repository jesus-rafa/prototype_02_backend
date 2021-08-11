from django.db import models
from django.db.models import Case, Count, F, Q, Sum, When, query


class OrderManager(models.Manager):

    def order_event(self, idEvent):

        return self.filter(
            event=idEvent,
        ).order_by('id')

    def summarize_event(self, idEvent):

        return self.filter(
            event=idEvent,
        ).annotate(
            sum_items=Count('quantity'),
            sum_amount=Sum('amount')
        ).order_by('id')

    def order_by_event_by_user(self, idEvent, idUser):

        return self.filter(
            event=idEvent,
            user=idUser
        )


# class OrderItemManager(models.Manager):

#     def order_event(self, idEvent):

#         return self.filter(
#             event=idEvent,
#         ).order_by('id')
