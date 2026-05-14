from django.test import TestCase
from django.urls import reverse


class AppointmentAuthTest(TestCase):

    def test_anonymous_user_cannot_create_appointment(self):
        response = self.client.get(reverse("appointments:create"))

        # обычно redirect на login
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)
