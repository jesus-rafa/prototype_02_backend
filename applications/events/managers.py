from os import stat

from django.db import models


class EventsManager(models.Manager):

    def events_by_user(self, idUser):

        return self.filter(
            create_by=idUser,
        ).order_by('created')

    def filter_events(self, status):

        if status == "EN PROCESO":
            status = ["EN PROCESO", "LLEGO PEDIDO"]
        elif status == "CONCLUIDO":
            status = ["CONCLUIDO"]

        return self.filter(
            status__in=status,
        ).order_by('created')
