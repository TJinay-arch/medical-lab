from django.urls import path

from .views import ServiceDetailView, ServicesView

app_name = "services"

urlpatterns = [
    path("services/", ServicesView.as_view(), name="services"),
    path("services/<int:pk>/", ServiceDetailView.as_view(), name="service_detail"),
]
