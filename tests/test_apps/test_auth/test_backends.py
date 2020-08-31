from tests.fixtures import UserFactory
from tests import faker
from django.contrib.auth import authenticate


def test_authenticate(db):
    user = UserFactory.build()
    password = faker.password()
    user.set_password(password)
    user.save()

    assert authenticate(username=user.username, password=password) == user
    assert authenticate(username=faker.user_name(), password=password) == None

    assert authenticate(username=user.email, password=password) == user
    assert authenticate(username=faker.email(), password=password) == None
