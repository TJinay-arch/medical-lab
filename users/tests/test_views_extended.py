# users/tests/test_views_extended.py
"""
Расширенные тесты для users/views.py
Цель: покрытие ~40 строк для достижения 75-90% общего coverage
"""
import pytest
from django.core import mail
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

User = get_user_model()


# ============================================================================
# 🔧 Глобальная фикстура: переключаем email-бэкенд на локальный для всех тестов
# ============================================================================
@pytest.fixture(autouse=True)
def use_locmem_email_backend(settings):
    """Переключаем email-бэкенд на locmem, чтобы письма не уходили реально"""
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


# ============================================================================
# 🔧 Фикстура: создание профиля врача (OneToOne relation)
# ============================================================================
@pytest.fixture
def doctor_profile_fixture(db):
    """
    Создаёт пользователя-врача с полным профилем.

    ⚠️ ВАЖНО: Проверьте, в каком приложении находится модель Doctor!
    Возможные варианты:
    - from core.models import Doctor
    - from appointments.models import Doctor
    - from users.models import Doctor
    """
    # 🔍 Раскомментируйте правильный импорт:
    from core.models import Doctor  # ← ПРОВЕРЬТЕ ЭТОТ ИМПОРТ!
    # from appointments.models import Doctor
    # from users.models import Doctor

    def _create_doctor_user(username="doctor_test", email="doc@test.com", password="pass123", **extra_fields):
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role="doctor",
            is_active=True,
            **extra_fields
        )
        # Создаём связанный профиль врача (OneToOne)
        Doctor.objects.create(
            user=user,
            first_name=extra_fields.get("first_name", "Test"),
            last_name=extra_fields.get("last_name", "Doctor"),
            specialization=extra_fields.get("specialization", "Therapist"),
            # 🔍 Добавьте здесь остальные обязательные поля вашей модели Doctor:
            # phone=extra_fields.get("phone", "+79991234567"),
            # birth_date=extra_fields.get("birth_date"),
            # ...
        )
        return user

    return _create_doctor_user


# ============================================================================
# 🧪 Тесты: ActivateUserView
# ============================================================================
@pytest.mark.django_db
class TestActivateUserView:
    """Тесты активации пользователя по ссылке из письма"""

    @pytest.fixture
    def inactive_user(self, db):
        """Создаёт неактивного пользователя для тестов активации"""
        return User.objects.create_user(
            username="activate_test",
            email="activate@test.com",
            password="pass123",
            is_active=False
        )

    def test_activate_success(self, client, inactive_user):
        """✅ Успешная активация: валидные uid+token"""
        uid = urlsafe_base64_encode(force_bytes(inactive_user.pk))
        token = default_token_generator.make_token(inactive_user)
        url = reverse("users:activate", kwargs={"uidb64": uid, "token": token})

        response = client.get(url, follow=True)

        inactive_user.refresh_from_db()
        assert inactive_user.is_active is True
        assert response.status_code == 200
        assert response.redirect_chain  # был хотя бы один редирект

    def test_activate_invalid_uid(self, client):
        """✅ Активация с несуществующим uid → редирект на логин"""
        fake_uid = urlsafe_base64_encode(force_bytes(99999))
        token = "fake-token"
        url = reverse("users:activate", kwargs={"uidb64": fake_uid, "token": token})

        response = client.get(url, follow=True)

        assert response.status_code == 200
        # Проверяем, что в цепочке редиректов есть логин
        assert any("login" in str(r[0]).lower() for r in response.redirect_chain)

    def test_activate_invalid_token(self, client, inactive_user):
        """✅ Активация с неверным токеном → редирект на логин"""
        uid = urlsafe_base64_encode(force_bytes(inactive_user.pk))
        fake_token = "invalid-token-123"
        url = reverse("users:activate", kwargs={"uidb64": uid, "token": fake_token})

        response = client.get(url, follow=True)

        inactive_user.refresh_from_db()
        assert inactive_user.is_active is False  # пользователь НЕ активирован
        assert response.status_code == 200
        assert any("login" in str(r[0]).lower() for r in response.redirect_chain)

    def test_activate_malformed_uid(self, client):
        """✅ Активация с битым uid (не декодируется) → редирект на логин"""
        url = reverse("users:activate", kwargs={"uidb64": "!!!invalid!!!", "token": "token"})
        response = client.get(url, follow=True)
        assert response.status_code == 200
        assert any("login" in str(r[0]).lower() for r in response.redirect_chain)


# ============================================================================
# 🧪 Тесты: dashboard_router (функция-маршрутизатор)
# ============================================================================
@pytest.mark.django_db
class TestDashboardRouter:
    """Тесты функции маршрутизации дашборда по роли пользователя"""

    def test_redirect_doctor(self, client, doctor_profile_fixture):
        """✅ Врач → doctor_dashboard"""
        doctor_user = doctor_profile_fixture()
        client.force_login(doctor_user)

        # 🔧 Не используем follow=True — проверяем сам редирект (статус 302)
        response = client.get(reverse("users:dashboard_router"))

        assert response.status_code == 302
        # Проверяем, что редирект ведёт на URL с doctor_dashboard
        assert "doctor_dashboard" in response.url or response.url == reverse("core:doctor_dashboard")

    def test_redirect_admin(self, client, db):
        """✅ Админ → appointments:list"""
        admin_user = User.objects.create_user(
            username="admin_test",
            email="admin@test.com",
            password="pass",
            role="admin",
            is_active=True
        )
        client.force_login(admin_user)
        response = client.get(reverse("users:dashboard_router"))

        assert response.status_code == 302
        assert "appointments" in response.url or response.url == reverse("appointments:list")

    def test_redirect_patient(self, client, db):
        """✅ Пациент → appointments:list"""
        patient_user = User.objects.create_user(
            username="patient_test",
            email="pat@test.com",
            password="pass",
            role="patient",
            is_active=True
        )
        client.force_login(patient_user)
        response = client.get(reverse("users:dashboard_router"))

        assert response.status_code == 302
        assert "appointments" in response.url or response.url == reverse("appointments:list")

    def test_requires_login(self, client):
        """✅ Неавторизованный доступ → редирект на логин"""
        response = client.get(reverse("users:dashboard_router"))
        # Django @login_required возвращает 302 (редирект) или 403
        assert response.status_code in (302, 403)


# ============================================================================
# 🧪 Тесты: RegisterView (дополнительные, покрываем form_valid)
# ============================================================================
@pytest.mark.django_db
class TestRegisterViewExtended:
    """Дополнительные тесты регистрации — покрываем form_valid()"""

    def test_registration_sends_email(self, client):
        """✅ После регистрации отправляется письмо активации"""
        response = client.post(
            reverse("users:register"),
            {
                "username": "email_test",
                "email": "email@test.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
            follow=True
        )
        # Проверяем, что письмо попало в outbox (не ушло реально)
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == "Подтверждение регистрации"
        assert "email@test.com" in mail.outbox[0].to
        # Опционально: проверить, что в теле есть ссылка активации
        assert "Подтвердите" in mail.outbox[0].body or "activation" in mail.outbox[0].body.lower()

    def test_registration_user_inactive(self, client):
        """✅ Новый пользователь создаётся с is_active=False"""
        client.post(
            reverse("users:register"),
            {
                "username": "inactive_test",
                "email": "inactive@test.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            }
        )
        user = User.objects.get(email="inactive@test.com")
        assert user.is_active is False

    def test_registration_success_message(self, client):
        """✅ После регистрации показывается сообщение через Django messages"""
        response = client.post(
            reverse("users:register"),
            {
                "username": "msg_test",
                "email": "msg@test.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
            follow=True
        )
        # Проверяем, что сообщение добавлено в контекст
        messages = list(response.context["messages"])
        assert any(
            "подтвердите" in str(m).lower() or "письмо" in str(m).lower()
            for m in messages
        )


# ============================================================================
# 🧪 Тесты: CustomLoginView
# ============================================================================
@pytest.mark.django_db
class TestCustomLoginView:
    """Тесты кастомного представления входа"""

    def test_login_page_has_title(self, client):
        """✅ Страница логина содержит context['title'] = 'Вход'"""
        response = client.get(reverse("users:login"))
        assert response.status_code == 200
        assert response.context["title"] == "Вход"


    def test_login_invalid_credentials(self, client):
        """✅ Неверный пароль → форма перерисовывается со статусом 200 и ошибками"""
        response = client.post(
            reverse("users:login"),
            {"username": "no_such_user", "password": "wrong"}
        )
        # При ошибке форма возвращается со статусом 200 (не редирект!)
        assert response.status_code == 200
        assert response.context["form"].errors  # форма должна содержать ошибки
