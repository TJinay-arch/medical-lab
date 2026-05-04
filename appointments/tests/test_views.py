from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser
from appointments.models import Appointment, Doctor, Service


class AppointmentViewTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@mail.com",
            password="12345"
        )

        self.client.force_login(self.user)

        # 🔥 ДОБАВИЛИ ЭТО
        self.doctor = Doctor.objects.create(
            first_name="Dr. House"
        )

        self.service = Service.objects.create(
            name="Consultation",
            price=1000
        )

    def test_create_appointment(self):
        response = self.client.post(
            reverse("appointments:create"),
            {
                "doctor": self.doctor.id,
                "service": self.service.id,
                "date": "2026-05-10",
                "time": "10:00",
                "status": "new",
            }
        )

        # если форма не прошла — сразу видно ошибку
        if response.status_code != 302:
            print(response.context["form"].errors)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Appointment.objects.count(), 1)


class AppointmentFlowTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="test",
            email="test@mail.com",
            password="12345"
        )

        self.client.force_login(self.user)

        self.doctor = Doctor.objects.create(first_name="Doc")
        self.service = Service.objects.create(name="Consultation", price=1000)

    def test_redirect_after_successful_create(self):
        response = self.client.post(reverse("appointments:create"), {
            "doctor": self.doctor.id,
            "service": self.service.id,
            "date": "2026-05-10",
            "time": "10:00",
            "status": "new",
        })

        self.assertEqual(response.status_code, 302)
