from django.urls import path
from .views import HomePageView, AboutView, ContactView, DoctorDetailView

app_name = "core"

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path("contacts/", ContactView.as_view(), name="contacts"),
    path("doctors/<int:pk>/", DoctorDetailView.as_view(), name="doctor_detail"),
]
