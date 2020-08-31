from django.contrib.auth.backends import ModelBackend
from server.apps.authentication.models import User


class CustomBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        f_kwargs = {}
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
            f_kwargs['username'] = username
        else:
            if '@' in username:
                f_kwargs['email'] = username
            else:
                f_kwargs['username'] = username

        if not f_kwargs or password is None:
            return

        try:
            user = User._default_manager.get(**f_kwargs)
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
