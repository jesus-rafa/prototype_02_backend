from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.dispatch import receiver
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
        blank=True
    )
    date_birth = models.DateField(
        'Fecha de nacimiento',
        blank=True,
        null=True
    )
    avatar = models.ImageField(
        'Avatar', blank=True, null=True, upload_to='users',)

    #
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['names']

    objects = UserManager()

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return self.names + ' ' + self.last_names

    def get_initials(self):
        return self.names[:1].upper() + self.last_names[:1].upper()


class Tribes(models.Model):
    """ Model Tribes """

    name = models.CharField('Nombre', max_length=300, unique=True)
    description = models.CharField(
        'Descripcion', max_length=400, blank=True, null=True)
    user = models.PositiveIntegerField(
        'Creado por', blank=True)
    is_active = models.BooleanField(default=True)
    avatar = models.ImageField(
        'Avatar Grupo', blank=True, null=True, upload_to='users',)
    members = models.ManyToManyField(
        User, blank=True, related_name='members'
    )

    objects = TribesManager()

    class Meta:
        verbose_name = 'Administrar Grupos'
        verbose_name_plural = 'Administrar Grupos'
        ordering = ['name']

    def __str__(self):
        return self.name


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(
        reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Software Machine"),
        # message:
        email_plaintext_message,
        # from:
        # "noreply@somehost.local",
        "rafalopezrl749@gmail.com",
        # to:
        [reset_password_token.user.email]
    )
