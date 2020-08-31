import factory
from server.apps.authentication import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
