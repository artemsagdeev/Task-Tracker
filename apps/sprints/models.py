from django.db import models
from apps.projects.models import Project

class Sprint(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='sprints',
    )

    start_date = models.DateField()

    end_date = models.DateField()

    goal = models.CharField(
        max_length=255,
    )

    class Meta:
        ordering = ['-start_date']