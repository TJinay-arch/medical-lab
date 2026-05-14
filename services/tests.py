from unittest.mock import patch

from django.test import TestCase

from appointments.models import Appointment, Doctor
from users.models import CustomUser


class EmailTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username="test", email="test@mail.com", password="123")

        self.doctor = Doctor.objects.create(first_name="House")

        self.appointment = Appointment.objects.create(user=self.user, doctor=self.doctor, date="2026-05-10 10:00")

    @patch("services.email.send_result_ready_email")
    def test_email_called(self, mock_email):
        mock_email.return_value = None

        mock_email(self.user, self.appointment)

        mock_email.assert_called_once()
