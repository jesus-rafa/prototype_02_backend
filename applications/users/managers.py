from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db.models import Count


class UserManager(BaseUserManager, models.Manager):

    def _create_user(self, email, names, last_names, password, is_staff, is_superuser, is_active, **extra_fields):
        user = self.model(
            email=email,
            names=names,
            last_names=last_names,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, names, last_names, password=None, **extra_fields):
        return self._create_user(email, names, last_names, password, True, False, True, **extra_fields)

    def create_superuser(self, email, names='', last_names='', password=None, **extra_fields):
        return self._create_user(email, names, last_names, password, True, True, True, **extra_fields)


class TribesManager(models.Manager):

    def tribes_by_user(self, idUser):

        return self.filter(
            user=idUser,
        ).order_by('id')

    def belong_to_tribes(self, idUser):

        return self.filter(
            members=idUser,
        )
