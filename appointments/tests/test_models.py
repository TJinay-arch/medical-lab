from datetime import date

from django.test import TestCase

from appointments.models import Appointment
from users.models import CustomUser


class AppointmentTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", email="test@mail.com", password="12345")

    def test_create_appointment(self):
        appointment = Appointment.objects.create(
            user=self.user,
            status="new",
            date=date(2026, 5, 10),
        )

        self.assertEqual(appointment.status, "new")
