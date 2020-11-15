from tests import fixtures, faker
from django.urls import reverse
from django.core.files.base import ContentFile
from server.apps.models import MediaFile, Post


def test_upload_image__success(db, api_client):
    user = fixtures.UserFactory.create()
    api_client.force_authenticate(user)
    photo = fixtures.create_image_data(size=(1080, 1920))
    photo_file = ContentFile(content=photo.getvalue(), name='photo.jpg')
    response = api_client.post(reverse('media'), data={'file': photo_file})
    assert response.status_code == 201
    media_obj = MediaFile.objects.get(uuid=response.data['uuid'])
    assert MediaFile.objects.get(uuid=response.data['uuid'])
    assert media_obj.file.read() == photo.getvalue()
    assert media_obj.owner == user
    assert media_obj.type == MediaFile.IMAGE


def test_upload_video__success(db, api_client):
    user = fixtures.UserFactory.create()
    api_client.force_authenticate(user)

    video_file = open(fixtures.TEST_VIDEO_PATH, 'rb')
    response = api_client.post(reverse('media'), data={'file': video_file})
    assert response.status_code == 201
    media_obj = MediaFile.objects.get(uuid=response.data['uuid'])
    assert MediaFile.objects.get(uuid=response.data['uuid'])
    video_file.seek(0)
    media_obj.file.seek(0)
    assert media_obj.file.read() == video_file.read()
    assert media_obj.owner == user
    assert media_obj.type == MediaFile.VIDEO
    video_file.close()


def test_new_post__success(db, api_client):
    user = fixtures.UserFactory.create()
    media_obj = fixtures.MediaFactory.create(owner=user)
    api_client.force_authenticate(user)

    post_data = {
        'media': media_obj.uuid,
        'text': faker.sentence()
    }
    response = api_client.post(reverse('posts'), data=post_data)
    assert response.status_code == 201
    post = Post.objects.get(uuid=response.data['uuid'])
    assert post
    assert post.text == post_data['text']
    assert post.owner == user
