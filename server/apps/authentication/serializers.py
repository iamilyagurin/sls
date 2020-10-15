from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse
from rest_framework import serializers
from .models import User


class SignUpUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):

    posts_url = serializers.SerializerMethodField('get_posts_url')

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'posts_url']
        extra_kwargs = {'password': {'write_only': True}}

    def get_posts_url(self, user_object):
        return reverse('user-posts', kwargs={'user_id': user_object.pk}, request=self.context['request'])

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'),
                            username=username, password=password)

        # The authenticate call simply returns None for is_active=False
        # users. (Assuming the default ModelBackend authentication
        # backend.)
        if not user:
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
