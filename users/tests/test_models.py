from django.test import TestCase
from users.models import CustomUser


class CustomUserModelTest(TestCase):

    def test_create_user(self):
        user = CustomUser.objects.create_user(
            username="testuser",
            email="test@mail.com",
            password="12345"
        )

        self.assertEqual(user.email, "test@mail.com")
        self.assertTrue(user.check_password("12345"))
        self.assertFalse(user.is_staff)
