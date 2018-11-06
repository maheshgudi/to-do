from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password


class LoginWithEmailBackend(object):
    """Takes email as the username when trying to authenticate user."""

    def authenticate(self, email=None, password=None):
        try:
          user = User.objects.get(email=email)
        except User.DoesNotExist:
          return None

        if check_password(password, user.password):
          return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

