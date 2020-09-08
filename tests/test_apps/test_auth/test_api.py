import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token

from tests import faker
from tests.fixtures import UserFactory
from server.apps.authentication.models import User


def test_get_auth_token__success(db, api_client):
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
    assert response.status_code == 200
    assert response.data['token'] == token.key

    # get exists
    response = api_client.post(
        reverse('auth-token'),
        data={
            'username': user.username,
            'password': password
        }
    )
    assert response.status_code == 200
    assert response.data['token'] == token.key


def test_get_auth_token__fail(db, api_client):
    response = api_client.post(
        reverse('auth-token'),
        data={
            'username': faker.user_name(),
            'password': faker.password()
        }
    )
    assert response.status_code == 400
    assert len(response.data['non_field_errors']) == 1


def test_sign_up__success(db, api_client):
    post_data = {
        'username': faker.user_name(),
        'email': faker.email(),
        'password': faker.password(),
    }
    response = api_client.post(
        reverse('sign-up'),
        data=post_data
    )
    assert response.status_code == 200
    assert Token.objects.get(key=response.data['token'])
    assert User.objects.get(
        username=post_data['username'],
        email=post_data['email'],
    ).check_password(post_data['password'])


def test_sign_up__fail(db, api_client):
    post_data = {
        'username': faker.user_name(),
        'email': faker.user_name(),
        'password': faker.password(),
    }
    response = api_client.post(
        reverse('sign-up'),
        data=post_data
    )
    assert response.status_code == 400
    assert User.objects.filter(
        username=post_data['username'],
        email=post_data['email'],
    ).count() == 0
    assert 'email' in response.data
