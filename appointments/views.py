from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.dateparse import parse_datetime
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.utils.timezone import now
from core.models import Doctor, Notification
from .models import Appointment, DiagnosticResult
from .forms import AppointmentForm, DiagnosticResultForm
from .services import get_available_slots
from services.email import send_notification_email, send_result_ready_email


class AppointmentCreateView(LoginRequiredMixin, CreateView):
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

        date = form.cleaned_data["date"]
        time = self.request.POST.get("time")

        dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")

        form.instance.date = dt
        doctor = form.instance.doctor
        if doctor and hasattr(doctor, "user") and doctor.user and doctor.user.email:
            send_notification_email(
                form.instance.doctor.user.email,
                "Новая запись на приём",
                f"У вас новая запись на {form.instance.date} от {self.request.user}"
            )

        return super().form_valid(form)


class DoctorSlotsAPIView(View):

    def get(self, request, *args, **kwargs):
        doctor_id = request.GET.get("doctor")
        date = request.GET.get("date")

        doctor = Doctor.objects.get(id=doctor_id)
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()

        slots = get_available_slots(doctor, date_obj)

        data = [
            slot.strftime("%H:%M")
            for slot in slots
        ]

        return JsonResponse(data, safe=False)


class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = "appointments/list.html"
    context_object_name = "appointments"

    def get_queryset(self):
        qs = Appointment.objects.filter(
            user=self.request.user
        ).select_related("doctor", "service").order_by("-date")

        filter_type = self.request.GET.get("filter")

        if filter_type == "upcoming":
            qs = qs.filter(date__gte=now())

        elif filter_type == "past":
            qs = qs.filter(date__lt=now())

        return qs


class AppointmentCancelConfirmView(DetailView):
    model = Appointment
    template_name = "appointments/cancel_confirm.html"
    context_object_name = "appointment"


class AppointmentCancelView(LoginRequiredMixin, View):

    def post(self, request, pk):
        appointment = get_object_or_404(
            Appointment,
            id=pk,
            user=request.user
        )

        appointment.status = Appointment.Status.CANCELED
        appointment.save()

        return redirect("appointments:list")


class AppointmentRescheduleView(LoginRequiredMixin, UpdateView):
    model = Appointment
    fields = []
    template_name = "appointments/reschedule.html"
    success_url = reverse_lazy("appointments:list")

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user)

    def form_valid(self, form):
        new_date = self.request.POST.get("date")

        if new_date:
            form.instance.date = parse_datetime(new_date)

        return super().form_valid(form)


class ResultDetailView(LoginRequiredMixin, DetailView):
    model = DiagnosticResult
    template_name = "appointments/result_detail.html"
    context_object_name = "result"


class DoctorResultUpdateView(LoginRequiredMixin, UpdateView):
    model = DiagnosticResult
    form_class = DiagnosticResultForm
    template_name = "appointments/doctor_result_form.html"

    def get_object(self):
        appointment_id = self.kwargs.get("appointment_id")

        appointment = get_object_or_404(
            Appointment,
            id=appointment_id,
            doctor=self.request.user.doctor_profile
        )

        obj, created = DiagnosticResult.objects.get_or_create(
            appointment=appointment
        )

        self.is_created = created
        return obj

    def form_valid(self, form):
        response = super().form_valid(form)

        appointment = self.object.appointment

        appointment.status = "done"
        appointment.save()

        Notification.objects.create(
            user=appointment.user,
            text=f"Результаты от {appointment.date.strftime('%d.%m %H:%M')} готовы"
        )

        try:
            send_result_ready_email(
                appointment.user,
                appointment
            )
        except Exception as e:
            print("❌ Ошибка при вызове email:", e)

        return response

    def get_success_url(self):
        return reverse_lazy("core:doctor_dashboard")
