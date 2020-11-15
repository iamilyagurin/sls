from rest_framework import serializers

from .bl import get_content_type
from .models import Post, MediaFile


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = ['uuid', 'file', 'type']
        extra_kwargs = {
            'file': {'write_only': True},
        }

    def to_internal_value(self, data):
        ct = get_content_type(data['file'])
        data['type'] = ct.split('/')[0]
        return super(MediaSerializer, self).to_internal_value(data)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['uuid', 'media', 'text', 'owner', 'url']
