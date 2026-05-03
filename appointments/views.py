from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Appointment
from .forms import AppointmentForm


class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "appointments/create.html"
    success_url = reverse_lazy("core:home")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs["doctor_id"] = self.request.GET.get("doctor")
        kwargs["service_id"] = self.request.GET.get("service")

        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user

        # если поле disabled → оно не отправляется → надо сохранить вручную
        doctor_id = self.request.GET.get("doctor")
        service_id = self.request.GET.get("service")

        if doctor_id:
            form.instance.doctor_id = doctor_id

        if service_id:
            form.instance.service_id = service_id

        return super().form_valid(form)

