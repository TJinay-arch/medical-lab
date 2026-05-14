from django.urls import path

from .views import (
    AppointmentCancelConfirmView,
    AppointmentCancelView,
    AppointmentCreateView,
    AppointmentListView,
    AppointmentRescheduleView,
    DoctorResultUpdateView,
    DoctorSlotsAPIView,
    ResultDetailView,
)

app_name = "appointments"

urlpatterns = [
    path("create/", AppointmentCreateView.as_view(), name="create"),
    path("api/slots/", DoctorSlotsAPIView.as_view(), name="slots"),
    path("my/", AppointmentListView.as_view(), name="list"),
    path("cancel/<int:pk>/", AppointmentCancelConfirmView.as_view(), name="cancel_confirm"),
    path("reschedule/<int:pk>/", AppointmentRescheduleView.as_view(), name="reschedule"),
    path("cancel/<int:pk>/confirm/", AppointmentCancelView.as_view(), name="cancel"),
    path("result/<int:pk>/", ResultDetailView.as_view(), name="result_detail"),
    path("doctor/result/<int:appointment_id>/", DoctorResultUpdateView.as_view(), name="doctor_result"),
]
