import unittest
from todoapp.todoutils import (EmailManipulation)

class TestEmailManipulation(unittest.TestCase):
    """Test email manipulation class"""

    @classmethod
    def setUpClass(self):
        self.email = "user@users.com"

    def test_correct_get_email_domain(self):
        """Test get_email_domain"""
        expected_email_output = "users.com"
        get_email = EmailManipulation.get_email_domain(self.email)
        self.assertEqual(expected_email_output, get_email)

    def test_incorrect_get_email_domain(self):
        """Test get_email_domain"""
        expected_email_output = "@users.com"
        get_email = EmailManipulation.get_email_domain(self.email)
        self.assertNotEqual(expected_email_output, get_email)
