import random
import string

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import (EmailMessage, EmailMultiAlternatives, send_mail,
                              send_mass_mail)
from django.db import models
from django.dispatch import receiver
from django.template.loader import get_template, render_to_string
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created

from .managers import TribesManager, UserManager


class User(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otros'),
    )

    email = models.EmailField(unique=True)
    names = models.CharField('Nombres', max_length=100)
    last_names = models.CharField('Apellidos', max_length=100)
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
        null=True
    )
    date_birth = models.DateField(
        'Fecha de nacimiento',
        blank=True,
        null=True
    )
    avatar = models.ImageField(
        'Avatar', blank=True, null=True, upload_to='users',
    )

    #
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['names']

    objects = UserManager()

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        if self.names:
            name = self.names + ' ' + self.last_names
        else:
            name = ''
        return name

    def get_initials(self):
        return self.names[:1].upper() + self.last_names[:1].upper()


class Tribes(models.Model):
    """ Model Tribes """

    name = models.CharField('Nombre', max_length=300, unique=True)
    description = models.CharField(
        'Descripcion', max_length=400, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='tribes_user', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    avatar = models.ImageField(
        'Avatar Grupo', blank=True, upload_to='users',)
    members = models.ManyToManyField(
        User,
        blank=True,
        related_name="members",
        through='Membership',
    )

    objects = TribesManager()

    class Meta:
        verbose_name = 'Administrar Grupos'
        verbose_name_plural = 'Administrar Grupos'
        ordering = ['name']

    def __str__(self):
        return self.name


class Membership(models.Model):
    group = models.ForeignKey(Tribes, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Miembros'
        verbose_name_plural = 'Miembros'
        ordering = ['id']
        unique_together = ('group', 'user',)


@ receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    # Envio de correo de restauración de contraseña
    subject = "Restauración de Contraseña {title}".format(title="App Eventos")
    text_content = ''
    html_content = render_to_string(
        'users/email/resetpassword_confirm.html',
        {'token': reset_password_token.key}
    )
    msg = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [reset_password_token.user.email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
