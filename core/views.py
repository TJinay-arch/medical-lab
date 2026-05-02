from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from .forms import ContactForm

from core.models import Doctor


class HomePageView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Главная — МедЦентр „Здоровье Плюс“'
        context['header_title'] = 'Добро пожаловать в МедЦентр „Здоровье Плюс“'
        context[
            'lead_text'] = 'Профессиональная медицинская помощь с заботой о вашем здоровье. Опытные врачи, современное оборудование и индивидуальный подход к каждому пациенту.'
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
    success_url = reverse_lazy("contacts")

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        subject = form.cleaned_data.get("subject")
        message = form.cleaned_data["message"]

        print(f"[CONTACT] {name} | {email} | {subject} | {message}")

        messages.success(self.request, "Сообщение успешно отправлено!")
        return super().form_valid(form)
