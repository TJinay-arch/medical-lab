from django.contrib import admin

from core.models import Doctor
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "phone_number", "country", "role")
    list_filter = ("country", "role",)
    search_fields = (
        "email",
        "phone_number",
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if obj.role == "doctor":
            Doctor.objects.get_or_create(user=obj)
