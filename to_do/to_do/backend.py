from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

class AuthenticationFailed(Exception):
    pass

class LoginWithEmailBackend(object):
    """Takes email instead of username as args when trying
       to authenticate user.
    """

    def authenticate(self, email=None, password=None):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise User.DoesNotExist("No user with this email-id")

        if user.check_password(password):
            return user
        else:
            raise AuthenticationFailed("The password did not match")

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise User.DoesNotExist("User does not exist")
