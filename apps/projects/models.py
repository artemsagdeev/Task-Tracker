from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Project(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Активен"
        FINISHED = "finished", "Закончен"
        ARCHIVED = "archived", "Архивирован"

    name = models.CharField(
        max_length=255
    )
    description = models.TextField(
        blank=True
    )

    start_date = models.DateField()

    end_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    members = models.ManyToManyField(
        User,
        related_name="projects",
        blank=True
    )