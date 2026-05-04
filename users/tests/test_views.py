from django.test import TestCase
from django.urls import reverse


class UserAuthTest(TestCase):

    def test_register_page_loads(self):
        response = self.client.get(reverse("users:register"))
        self.assertEqual(response.status_code, 200)

    def test_user_registration(self):
        response = self.client.post(reverse("users:register"), {
            "username": "testuser",
            "email": "test@mail.com",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
        })

        self.assertEqual(response.status_code, 302)  # redirect
