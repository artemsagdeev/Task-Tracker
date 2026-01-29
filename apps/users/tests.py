import pytest
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_register_requires_email(api_client):
    response = api_client.post(
        '/api/auth/register/',
        {
            'username': 'user',
            'password': 'password123',
        }, format='json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'email' in response.data['error']['details']

@pytest.mark.django_db
def test_register_email_unique(api_client):
    User.objects.create_user(
        username='user1',
        email='test@example.com',
        password='password123',
    )

    response = api_client.post(
        '/api/auth/register/',
        {
            'username': 'user2',
            'email': 'test@example.com',
            'password': 'password123',
        }, format='json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'email' in response.data['error']['details']