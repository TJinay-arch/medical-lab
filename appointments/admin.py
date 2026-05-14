# appointments/admin.py

from django.contrib import admin

from services.email import send_notification_email

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "doctor", "service", "date", "created_at")
    list_filter = ("doctor", "service", "date")
    search_fields = ("user__email", "doctor__name", "service__name")
    ordering = ("-created_at",)

    def save_model(self, request, obj, form, change):
        if change:
            old = Appointment.objects.get(pk=obj.pk)

            # ОТМЕНА
            if old.status != obj.status and obj.status == "canceled":
                send_notification_email(
                    obj.user.email, "Запись отменена", f"Ваша запись на {obj.date} была отменена администратором."
                )

            # ПЕРЕНОС
            if old.date != obj.date:
                send_notification_email(obj.user.email, "Запись перенесена", f"Ваша запись перенесена на {obj.date}")

        super().save_model(request, obj, form, change)
