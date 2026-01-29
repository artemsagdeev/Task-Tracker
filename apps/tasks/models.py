from django.contrib.auth import get_user_model
from django.db import models
from apps.sprints.models import Sprint
from api.enums import TaskStatus

User = get_user_model()

class Task(models.Model):
    class Type(models.TextChoices):
        FEATURE = 'feature', 'Фича'
        BUG = 'bug', 'Баг'
        TECH_DEBT = 'tech_debt', 'Технический долг'
        DOCUMENTATION = 'documentation', 'Документация'

    class Priority(models.TextChoices):
        CRITICAL = 'critical', 'Критичный'
        HIGH = 'high', 'Высокий'
        MEDIUM = 'medium', 'Средний'
        LOW = 'low', 'Маленький'

    title = models.CharField(
        max_length=255
    )

    description = models.TextField()

    type = models.CharField(
        max_length=20,
        choices=Type.choices,
    )
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
    )

    status = models.CharField(
        max_length=30,
        choices=TaskStatus.choices,
        default=TaskStatus.OPEN,
    )

    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks',
    )

    sprint = models.ForeignKey(
        Sprint,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks',
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )