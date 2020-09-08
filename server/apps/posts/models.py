from django.db import models
from server.apps.authentication.models import User
import uuid
# Create your models here.



class Post(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False,
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    content = models.FileField()
    description = models.TextField()
