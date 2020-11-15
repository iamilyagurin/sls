import magic
from django.core.files.uploadedfile import UploadedFile

from .models import MediaFile


def process_media(media_obj: MediaFile):
    if media_obj.type == MediaFile.IMAGE:
        media_obj.generate_thumbs()
    elif media_obj.type == MediaFile.VIDEO:
        # TODO: process video
        pass


def get_content_type(file: UploadedFile):
    content_type = magic.from_buffer(file.read(), mime=True)
    file.seek(0)
    return content_type


def content_type_magic_set(file: UploadedFile):
    setattr(file, 'content_type_magic', get_content_type(file))
    return file
