import pytest
from rest_framework.test import APIClient
from api.enums import UserRole, TaskStatus
from apps.users.models import User
from apps.projects.models import Project
from apps.sprints.models import Sprint
from apps.tasks.models import Task

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def manager():
    return User.objects.create_user(
        username='manager',
        email='manager@test.com',
        password='password123',
        role=UserRole.MANAGER,
    )

@pytest.fixture
def developer():
    return User.objects.create_user(
        username='developer',
        email='developer@test.com',
        password='password123',
        role=UserRole.DEVELOPER,
    )

@pytest.fixture
def project(manager):
    project = Project.objects.create(
        name='Test Project',
        start_date='2026-01-01',
        end_date='2026-02-01',
    )
    return project

@pytest.fixture
def sprint(project):
    return Sprint.objects.create(
        project=project,
        start_date='2026-01-01',
        end_date='2026-01-14',
        goal='Sprint goal',
    )

@pytest.fixture
def task(sprint, developer):
    return Task.objects.create(
        title='Test Task',
        description='Description',
        type='feature',
        priority='high',
        sprint=sprint,
        assignee=developer,
        status=TaskStatus.IN_PROGRESS,
    )