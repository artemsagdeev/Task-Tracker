from django.contrib.auth.models import AbstractUser
from django.db import models
from api.enums import UserRole

class User(AbstractUser):

    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        null=True,
        blank=True
    )

    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )

    def is_manager(self):
        return self.role == UserRole.MANAGER

    def is_developer(self):
        return self.role == UserRole.DEVELOPER

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


