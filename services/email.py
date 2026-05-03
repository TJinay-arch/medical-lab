from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string


def send_notification_email(to_email, subject, message):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [to_email],
        fail_silently=False,
    )


def send_result_ready_email(user, appointment):
    if not user or not user.email:
        print("❌ Email не отправлен: нет пользователя или email")
        return

    subject = "Результаты готовы — Здоровье Плюс"

    context = {
        "user": user,
        "appointment": appointment,
    }

    try:
        html_content = render_to_string(
            "emails/result_ready.html",
            context
        )

        msg = EmailMultiAlternatives(
            subject=subject,
            body="Ваши результаты готовы. Зайдите в личный кабинет.",
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email]
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()

        print(f"✅ Email отправлен на {user.email}")

    except Exception as e:
        print("❌ Ошибка отправки email:", e)
