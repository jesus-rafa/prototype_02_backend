from django.db import models


class EventsManager(models.Manager):

    def events_by_user(self, idUser):

        return self.filter(
            create_by=idUser,
        ).order_by('created')
