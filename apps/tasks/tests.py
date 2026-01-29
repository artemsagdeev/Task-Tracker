import pytest
from api.enums import TaskStatus
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_full_task_lifecycle(api_client, manager, developer, sprint):
    api_client.force_authenticate(manager)
    response = api_client.post(
        '/api/tasks/',
        {
            'title': 'Lifecycle task',
            'description': 'Test',
            'type': 'feature',
            'priority': 'high',
            'sprint': sprint.id,
        }, format='json',
    )
    assert response.status_code == 201
    task_id = response.data['data']['id']
    response = api_client.patch(
        f'/api/tasks/{task_id}/status/',
        {"status": TaskStatus.SELECTED},
        format='json',
    )
    assert response.status_code == 200

    response = api_client.post(
        f'/api/tasks/{task_id}/assign/',
        {'user': developer.id},
        format='json',
    )
    assert response.status_code == 200
    assert response.data['data']['assignee']['id'] == developer.id
    api_client.force_authenticate(developer)
    response = api_client.patch(
        f'/api/tasks/{task_id}/status/',
        {'status': TaskStatus.IN_PROGRESS},
        format='json',
    )
    assert response.status_code == 200
    assert response.data['data']['status'] == TaskStatus.IN_PROGRESS
    response = api_client.patch(
        f'/api/tasks/{task_id}/status/',
        {'status': TaskStatus.READY_TO_ACCEPTANCE},
        format='json',
    )
    assert response.status_code == 200
    assert response.data['data']['status'] == TaskStatus.READY_TO_ACCEPTANCE
    api_client.force_authenticate(manager)
    response = api_client.patch(
        f'/api/tasks/{task_id}/status/',
        {'status': TaskStatus.CLOSED},
        format='json',
    )
    assert response.status_code == 200
    assert response.data['data']['status'] == TaskStatus.CLOSED


@pytest.mark.django_db
def test_developer_cannot_create_task(api_client, developer, sprint):
    api_client.force_authenticate(developer)

    response = api_client.post(
        '/api/tasks/',
        {
            'title': 'Invalid',
            'description': 'No rights',
            'type': 'bug',
            'priority': 'low',
            'sprint': sprint.id,
        },
        format='json',
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_developer_cannot_close_task(api_client, developer, task):
    api_client.force_authenticate(developer)

    response = api_client.patch(
        f'/api/tasks/{task.id}/status/',
        {'status': TaskStatus.CLOSED},
        format='json',
    )

    assert response.status_code == 400