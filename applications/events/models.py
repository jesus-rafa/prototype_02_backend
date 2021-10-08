from applications.users.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel

from .managers import EventsManager


class Event(TimeStampedModel):
    ''' Event Model '''

    name = models.CharField(
        'Nombre',
        max_length=200,
    )
    description = models.CharField(
        'Descripcion',
        max_length=254,
    )
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  related_name='event_user', on_delete=models.CASCADE)
    date_start = models.DateField('Fecha Inicio', blank=True)
    date_end = models.DateField('Fecha Fin', blank=True, null=True)
    hour_start = models.TimeField('Hora Inicio', blank=True, null=True)
    hour_end = models.TimeField('Hora Fin', blank=True, null=True)
    status = models.CharField(
        'Estatus',
        max_length=100,
        blank=True,
    )
    image = models.ImageField(
        'Imagen', blank=True, null=True, upload_to='events',)
    is_active = models.BooleanField(default=True)
    participants = models.ManyToManyField(
        User,
        blank=True,
        related_name="list_members",
        through='Participants',
    )

    objects = EventsManager()

    class Meta:
        verbose_name = 'Eventos'
        verbose_name_plural = 'Eventos'

    def __str__(self):
        return self.name


class Event_Detail(TimeStampedModel):
    ''' Event_Detail Model '''

    name = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='detail_event')
    content = RichTextUploadingField('Contenido', blank=True)
    image1 = models.ImageField(
        'Imagen 1', blank=True, null=True, upload_to='events',)
    image2 = models.ImageField(
        'Imagen 2', blank=True, null=True, upload_to='events',)
    image3 = models.ImageField(
        'Imagen 3', blank=True, null=True, upload_to='events',)
    image4 = models.ImageField(
        'Imagen 4', blank=True, null=True, upload_to='events',)
    file = models.FileField(
        'Archivo',
        upload_to='events',
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Detalle Eventos'
        verbose_name_plural = 'Detalle Eventos'

    def __str__(self):
        return str(self.name)


class Participants(models.Model):
    name = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='participants_event'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    is_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Participantes'
        verbose_name_plural = 'Participantes'
        unique_together = ('name', 'user',)

    def __str__(self):
        return str(self.name)
