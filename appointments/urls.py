from django.urls import path
from .views import AppointmentCreateView

app_name = "appointments"

urlpatterns = [
    path("create/", AppointmentCreateView.as_view(), name="create"),
]