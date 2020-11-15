import factory

from server.apps import models
from .image import create_image_data
from .media import TEST_MEDIA_DIR, TEST_VIDEO_PATH
from .user import UserFactory


class MediaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.MediaFile

    owner = factory.SubFactory(UserFactory)
