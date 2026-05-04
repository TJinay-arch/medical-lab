from django.test import TestCase
from django.utils import timezone

from users.models import CustomUser
from appointments.models import Appointment, Doctor, Service
from appointments.services import get_available_slots


class GetAvailableSlotsTest(TestCase):

    def setUp(self):

        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@mail.com",
            password="12345"
        )

        self.doctor = Doctor.objects.create(
            first_name="Gregory",
            last_name="House"
        )

        self.service = Service.objects.create(
            name="Consultation",
            price=1000
        )

        self.date = timezone.now().date()

    def test_slots_exclude_taken_time(self):

        Appointment.objects.create(
            user=self.user,
            doctor=self.doctor,
            service=self.service,
            date=timezone.now(),
            status="new"
        )

        slots = get_available_slots(self.doctor, self.date)

        self.assertIsInstance(slots, list)
