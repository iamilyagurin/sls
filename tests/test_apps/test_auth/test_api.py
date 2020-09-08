import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token

from tests import faker
from tests.fixtures import UserFactory


def test_get_auth_token__success(transactional_db, api_client):
    password = faker.password()
    user = UserFactory.build()
    user.set_password(password)
    user.save()

    with pytest.raises(Token.DoesNotExist):
        Token.objects.get(user_id=user.id)

    # first create
    response = api_client.post(
        reverse('auth-token'),
        data={
            'username': user.username,
            'password': password
        }
    )
    token = Token.objects.get(user_id=user.id)
    assert response.data['token'] == token.key

    # get exists
    response = api_client.post(
        reverse('auth-token'),
        data={
            'username': user.username,
            'password': password
        }
    )
    assert response.data['token'] == token.key


def test_get_auth_token__errors(transactional_db, api_client):
    response = api_client.post(
        reverse('auth-token'),
        data={
            'username': faker.user_name(),
            'password': faker.password()
        }
    )
    assert len(response.data['non_field_errors']) == 1

