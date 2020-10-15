from django.db import models
from server.apps.authentication.models import User
import uuid



class MediaFile(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    file = models.FileField(upload_to='post/origin')


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
