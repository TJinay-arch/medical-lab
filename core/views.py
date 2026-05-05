from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.utils import translation
from django.utils.formats import date_format
from django.views.generic import DetailView, FormView, TemplateView

from appointments.models import Appointment
from core.models import Doctor, Notification

from .forms import ContactForm


class HomePageView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Главная — МедЦентр „Здоровье Плюс“"
        context["header_title"] = "Добро пожаловать в МедЦентр „Здоровье Плюс“"
        context["lead_text"] = (
            "Профессиональная медицинская помощь с заботой о вашем здоровье. "
            "Опытные врачи, современное оборудование и индивидуальный подход к каждому пациенту."
        )
        context["form"] = ContactForm()
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
        translation.activate("ru")
        # только врач
        if user.role != "doctor":
            return context

        doctor = user.doctor_profile

        # уведомления
        context["notifications"] = Notification.objects.filter(user=user).order_by("-created_at")[:10]

        # записи врача
        filter_type = self.request.GET.get("filter", "active")
        page_number = self.request.GET.get("page", 1)

        appointments = Appointment.objects.filter(doctor=doctor)

        if filter_type == "active":
            appointments = appointments.filter(status__in=["new", "confirmed"])
        elif filter_type == "done":
            appointments = appointments.filter(status="done")

        appointments = appointments.order_by("date")

        paginator = Paginator(appointments, 4)
        page_obj = paginator.get_page(page_number)

        # группировка только текущей страницы
        grouped = {}

        for app in page_obj:
            day = date_format(app.date, "l, j E")
            grouped.setdefault(day, []).append(app)

        context["appointments_by_day"] = grouped
        context["page_obj"] = page_obj
        context["filter"] = filter_type

        return context
