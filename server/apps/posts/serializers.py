from rest_framework import serializers
from .models import Post, MediaFile



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['uuid', 'media', 'text', 'owner', 'url']


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = ['uuid', 'file']

