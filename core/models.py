from django.db import models

from users.models import CustomUser


class Doctor(models.Model):
    SPECIALIZATIONS = [
        ("therapist", "Терапевт"),
        ("cardiologist", "Кардиолог"),
        ("pediatrician", "Педиатр"),
        ("neurologist", "Невролог"),
        ("lab", "Лабораторная диагностика"),
    ]
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="doctor_profile",
        null=True,
        blank=True
    )
    first_name = models.CharField("Имя", max_length=50)
    last_name = models.CharField("Фамилия", max_length=50)

    specialization = models.CharField(
        "Специализация",
        max_length=50,
        choices=SPECIALIZATIONS
    )

    experience_years = models.PositiveIntegerField("Стаж (лет)", default=0)

    photo = models.ImageField(
        "Фото",
        upload_to="doctors/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField("Активен", default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
