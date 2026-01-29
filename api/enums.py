from django.db import models

class UserRole(models.TextChoices):
    MANAGER = 'manager', 'Менеджер'
    DEVELOPER = 'developer', 'Разработчик'


class TaskStatus(models.TextChoices):
    OPEN = 'open', 'Открыт'
    SELECTED = 'selected', 'Выбран'
    IN_PROGRESS = 'in_progress', 'В прогрессе'
    READY_TO_ACCEPTANCE = 'ready_to_acceptance', 'Готово к принятию'
    CLOSED = 'closed', 'Закрыто'