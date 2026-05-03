from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.views.generic import CreateView

from .forms import CustomUserCreationForm, LoginForm
from django.views import View
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login, get_user_model

User = get_user_model()


class ActivateUserView(View):

    def get(self, request, uidb64, token):

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except Exception:
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            login(request, user)

            return redirect("core:home")

        return redirect("users:login")


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = "users/login.html"
    success_url = reverse_lazy("core:home")

    def get_success_url(self):
        return self.success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Вход"
        return context


class CustomLogoutView(LogoutView):
    template_name = "core/home.html"
    next_page = None


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "users/registration.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        activation_link = self.request.build_absolute_uri(
            reverse("users:activate", kwargs={
                "uidb64": uid,
                "token": token
            })
        )

        html_content = render_to_string("emails/activation_email.html", {
            "user": user,
            "activation_link": activation_link,
        })

        email = EmailMultiAlternatives(
            subject="Подтверждение регистрации",
            body="Подтвердите регистрацию по ссылке",  # fallback
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )

        email.attach_alternative(html_content, "text/html")
        email.send()
        messages.success(
            self.request,
            "Мы отправили письмо на вашу почту. Подтвердите регистрацию."
        )
        return redirect(self.success_url)

@login_required
def dashboard_router(request):
    user = request.user

    if user.role == "doctor":
        return redirect("core:doctor_dashboard")

    if user.role == "admin":
        return redirect("appointments:list")

    # пациент
    return redirect("appointments:list")