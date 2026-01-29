import pytest

@pytest.mark.django_db
def test_sprint_outside_project_dates(api_client, manager, project):
    api_client.force_authenticate(manager)
    response = api_client.post(
        '/api/sprints/',
        {
            'project': project.id,
            'start_date': '2023-12-01',
            'end_date': '2023-12-10',
            'goal': 'Invalid sprint',
        }, format='json',
    )

    assert response.status_code == 400
    assert response.data['success'] is False


