from collections import defaultdict

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, DetailView

from appointments.models import Appointment
from users.mixins import RoleRequiredMixin
from .forms import ContactForm

from core.models import Doctor, Notification


class HomePageView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Главная — МедЦентр „Здоровье Плюс“'
        context['header_title'] = 'Добро пожаловать в МедЦентр „Здоровье Плюс“'
        context[
            'lead_text'] = 'Профессиональная медицинская помощь с заботой о вашем здоровье. Опытные врачи, современное оборудование и индивидуальный подход к каждому пациенту.'
        context['form'] = ContactForm()
        return context


class AboutView(TemplateView):
    template_name = "core/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["doctors"] = Doctor.objects.filter(is_active=True)

        return context


class ContactView(FormView):
    template_name = "core/contacts.html"
    form_class = ContactForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        subject = form.cleaned_data.get("subject")
        message = form.cleaned_data["message"]

        print(f"[CONTACT] {name} | {email} | {subject} | {message}")

        messages.success(self.request, "Сообщение успешно отправлено!")
        return super().form_valid(form)


class DoctorDetailView(DetailView):
    model = Doctor
    template_name = "core/doctor_detail.html"
    context_object_name = "doctor"


class DoctorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        # только врач
        if user.role != "doctor":
            return context

        doctor = user.doctor_profile

        # уведомления
        context["notifications"] = Notification.objects.filter(
            user=user
        ).order_by("-created_at")[:10]

        # записи врача
        appointments = Appointment.objects.filter(
            doctor=doctor
        ).order_by("date")

        # группировка по дням
        grouped = {}

        for app in appointments:
            day = app.date.date()
            grouped.setdefault(day, []).append(app)

        context["appointments_by_day"] = grouped

        return context
