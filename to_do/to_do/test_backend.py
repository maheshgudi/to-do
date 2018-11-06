import unittest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from to_do.backend import AuthenticationFailedException

def setUpModule():
    user = User.objects.create_user(username="user",
                                    email="user@users.com",
                                    password="user"
                                    )

def tearDownModule():
    User.objects.get(username="user").delete()


class AuthenticationTestCase(unittest.TestCase):
    """Test authentication backend """

    @classmethod
    def setUpClass(self):
        self.user1 = User.objects.get(username="user")

    def test_authentication_with_correct_email(self):
        user_email = "user@users.com"
        user_password = "user"
        user = authenticate(email=user_email, password=user_password)
        self.assertEqual(user, self.user1)

    def test_authentication_with_incorrect_email(self):
        user_email = "nouser@users.com"
        user_password = "user"
        with self.assertRaises(User.DoesNotExist):
            user = authenticate(email=user_email, password=user_password)

    def test_authentication_with_incorrect_password(self):
        user_email = "user@users.com"
        user_password = "user123"
        with self.assertRaises(AuthenticationFailedException):
            user = authenticate(email=user_email, password=user_password)
