# appointments/admin.py

from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "doctor", "service", "date", "created_at")
    list_filter = ("doctor", "service", "date")
    search_fields = ("user__email", "doctor__name", "service__name")
    ordering = ("-created_at",)
