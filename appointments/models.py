from django.db import models
from django.conf import settings
from core.models import Doctor
from services.models import Service


class Appointment(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новая"
        CONFIRMED = "confirmed", "Подтверждена"
        DONE = "done", "Завершена"
        CANCELED = "canceled", "Отменена"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        related_name="appointments"
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        related_name="appointments"
    )

    date = models.DateTimeField()
    comment = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} → {self.service} ({self.date})"
