from django.db import models
from server.apps.authentication.models import User
import uuid
from PIL import ImageOps, Image
import io
from django.core.files.base import File
from typing import Tuple

__all__ = ['MediaFile', 'Post']

def _size_name(size: Tuple[int, int]):
    return "{0}x{1}".format(*size)


def get_thumb_path(name: str, size: Tuple[int, int]):
    size_name = _size_name(size)
    return f'post/{size_name}/{name}'



class MediaFile(models.Model):
    IMAGE = 'image'
    VIDEO = 'video'
    TYPES = (
        (IMAGE, IMAGE),
        (VIDEO, VIDEO),
    )

    THUMB_SIZE = (640, 1400)

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, editable=False)
    file = models.FileField(upload_to='post/origin')
    type = models.CharField(max_length=5, choices=TYPES, null=False)

    @property
    def thumb_name(self):
        return f'{self.uuid}.jpg'

    @property
    def thumb_path(self):
        return get_thumb_path(self.thumb_name, self.THUMB_SIZE)

    def url(self):
        return self.file.storage.url(self.thumb_path)

    def generate_thumbs(self) -> None:
        im = Image.open(self.file.file)
        if im.mode in ("RGBA", "P"):
            im = im.convert("RGB")
        im = ImageOps.exif_transpose(im)
        im.thumbnail(self.THUMB_SIZE)
        image_file = io.BytesIO()
        im.save(image_file, 'jpeg', optimize=True, quality=85)
        self.file.storage.save(self.thumb_path, File(image_file))


class Post(models.Model):
    class Meta:
        db_table = "post"

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    media = models.ForeignKey(MediaFile, on_delete=models.PROTECT)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True, null=True)
