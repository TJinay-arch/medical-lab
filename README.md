# 🏥 Medical Lab
## Backend-приложение для медицинской лаборатории
Django-приложение для управления записями пациентов, назначениями врачей, услугами и результатами диагностики. Поддерживает роли: Пациент, Врач, Администратор.
### 📋 Оглавление
- 🚀 Быстрый старт
- 🐳 Установка и запуск в Docker
- ⚙️ Локальная установка (без Docker)
- 📁 Структура проекта
- 🔑 Основные функции
- 🧪 Тестирование
- 📧 Настройка email-уведомлений
- 🔐 Переменные окружения

### 🚀 Быстрый старт
#### 1. Клонируйте репозиторий
``` 
git clone -b feature/basic_settings https://github.com/TJinay-arch/medical-lab.git
```
```
cd medical-lab
```
#### 2. Создайте файл окружения
```
cp .env.sample .env
```
#### Отредактируйте .env, указав реальные значения

#### 3. Запустите через Docker
 ```
docker-compose up --build
```
#### 4. Откройте в браузере
```
http://localhost]
```

### 🐳 Установка и запуск в Docker
Требования
+ Docker >= 20.10
+ Docker Compose >= 1.29

Шаг 1: Настройка переменных окружения

Создайте файл .env в корне проекта на основе .env.sample:
```
cp .env.sample .env
```
Заполните файл .env:
```commandline
# Django
SECRET_KEY=your-super-secret-key-here
DEBUG=True

# PostgreSQL
POSTGRES_DB=medical_lab
POSTGRES_USER=medical_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Email (для уведомлений)
PASSWORD_FOR_MAIL=your-app-password
```

⚠️ Важно: В продакшене используйте сложные пароли и храните .env в секретах, а не в репозитории.

Шаг 2: Сборка и запуск контейнеров
```commandline
# Сборка и запуск всех сервисов
docker-compose up --build -d

# Просмотр логов
docker-compose logs -f web

# Остановка
docker-compose down
```

Шаг 3: Применение миграций и создание суперпользователя
```commandline
# Применение миграций (автоматически в entrypoint, но можно вручную)
docker-compose exec web python manage.py migrate

# Создание суперпользователя
docker-compose exec web python manage.py createsuperuser

# Сбор статики (если нужно)
docker-compose exec web python manage.py collectstatic --noinput
```

##### Архитектура Docker-окружения
```commandline
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   nginx:80      │────▶│   web:8000      │────▶│   db:5432       │
│   (reverse      │     │   (Django +     │     │   (PostgreSQL   │
│    proxy)       │     │    Gunicorn)    │     │    15)          │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
  http://localhost     gunicorn:0.0.0.0:8000    postgres_data volume
  static: /static      media: /media
```
Сервисы:
+ Nginx ― веб-сервер (порт 80);
+ web – Python-сервис (порт 8000, внутренний);
+ db– база данных PostgresSQL (порт 5432, внутренний)

Volumes:
+ postgres_data — хранение БД
+ static_volume — собранные статические файлы
+ media_volume — загруженные пользователями файлы (аватары, результаты анализов)

#### ⚙️ Локальная установка (без Docker)

Требования
+ Python 3.13
+ Poetry (менеджер зависимостей)
+ PostgreSQL 15+

Шаг 1: Установка Poetry и зависимостей

```commandline
# Установка Poetry (если не установлен)
curl -sSL https://install.python-poetry.org | python3 -

# Установка зависимостей
poetry install

# Активация виртуального окружения
poetry shell
```

Шаг 2: Настройка окружения и БД
```commandline
# Копирование .env
cp .env.sample .env
# Отредактируйте .env под вашу локальную среду

# Запуск миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Сбор статики (для production-режима)
python manage.py collectstatic --noinput
```
Шаг 3: Запуск сервера разработки
 ```
 # Запуск Django-сервера
python manage.py runserver

# 👉 Приложение доступно по адресу: http://127.0.0.1:8000
 ```

### 📁 Структура проекта
```commandline
medical-lab/
├── config/                 # Настройки Django-проекта
│   ├── settings.py         # Основные настройки (БД, email, middleware)
│   ├── urls.py             # Корневая маршрутизация
│   ├── wsgi.py             # WSGI-конфигурация для Gunicorn
│   └── asgi.py             # ASGI-конфигурация (на будущее)
│
├── core/                   # Ядро приложения
│   ├── models.py           # Общие модели (Doctor, Notification)
│   ├── services.py         # Базовые сервисы (уведомления)
│   ├── views.py            # Главные страницы, дашборды
│   └── urls.py             # Маршруты ядра
│
├── users/                  # Модуль пользователей и авторизации
│   ├── models.py           # CustomUser с ролями и полями
│   ├── forms.py            # Формы регистрации и входа
│   ├── views.py            # Регистрация, активация, вход/выход
│   ├── mixins.py           # Миксины для ограничения доступа по ролям
│   ├── urls.py             # Auth-маршруты
│   └── tests/              # Тесты пользователей
│       ├── test_models.py
│       ├── test_views.py
│       └── test_forms.py
│
├── appointments/           # Модуль записей и приёмов
│   ├── models.py           # Appointment, DiagnosticResult
│   ├── services.py         # Логика слотов времени, доступности врачей
│   ├── views.py            # CRUD для записей, календарь
│   ├── urls.py             # Маршруты записей
│   └── tests/              # Тесты бизнес-логики
│       ├── test_models.py
│       ├── test_services.py
│       ├── test_views.py
│       └── test_business_rules.py
│
├── services/               # Модуль медицинских услуг
│   ├── models.py           # Service (название, цена, описание)
│   ├── views.py            # Список и детализация услуг
│   └── urls.py             # Маршруты услуг
│
├── docker/                 # Docker-конфигурации
│   ├── django/
│   │   ├── Dockerfile      # Образ Python 3.13 + Poetry + зависимости
│   │   └── entrypoint.sh   # Инициализация: миграции, collectstatic, запуск
│   └── nginx/
│       └── nginx.conf      # Конфигурация reverse proxy
│
├── templates/              # HTML-шаблоны (Jinja2/Django)
│   ├── emails/             # Шаблоны писем (активация, уведомления)
│   ├── users/              # Страницы авторизации
│   └── appointments/       # Формы записи, календарь
│
├── static/                 # Статические файлы (CSS, JS, изображения)
├── media/                  # Загружаемые файлы (аватары, результаты)
│
├── docker-compose.yml      # Оркестрация контейнеров
├── pyproject.toml          # Зависимости Poetry и настройки линтеров
├── poetry.lock             # Зафиксированные версии зависимостей
├── manage.py               # Django management script
├── .env.sample             # Шаблон переменных окружения
└── .gitignore              # Исключения для Git
```

### 🔑 Основные функции
#### 👥 Система пользователей и ролей
+ Кастомная модель пользователя (CustomUser) на базе AbstractUser
+ Роли: patient, doctor, admin (через TextChoices)
+ Аутентификация по email (USERNAME_FIELD = "email")
+ Подтверждение регистрации через ссылку с токеном
+ Профиль пользователя: аватар, телефон, страна
#### 📅 Запись на приём (Appointments)
+ Модель Appointment с полями:
+ Пациент (user), Врач (doctor), Услуга (service)
+ Дата/время, комментарий, статус
+ Статусы записи: new → confirmed → done / canceled
+ Генерация временных слотов (9:00–18:00, шаг 30 минут)
+ Проверка доступности врача на выбранную дату
+ Связь с результатом диагностики через OneToOneField
#### 🧾 Результаты диагностики
+ Модель DiagnosticResult:
+ Текстовое заключение врача
+ Прикреплённый файл (PDF, изображения)
+ Привязка к конкретной записи
#### 🩺 Услуги и врачи
+ Модель Service: название, описание, цена
+ Связь многие-ко-многим между услугами и врачами
+ Модель Doctor (в core) — расширение пользователя для врачей
#### 🔔 Уведомления
Email-уведомления при:
+ Подтверждении регистрации
+ Изменении статуса записи
+ Добавлении результата диагностики
+ Внутренние уведомления (Notification модель) для отображения в интерфейсе
###### SMTP-настройка через Mail.ru (настраивается в .env)
#### 🎛️ Админ-панель
+ Полноценная Django Admin с регистрацией всех моделей
+ Фильтрация записей по статусу, дате, врачу
+ Управление пользователями и услугами

### 🧪 Тестирование
Запуск тестов
```commandline
# Все тесты
docker-compose exec web python manage.py test

# Тесты конкретного приложения
docker-compose exec web python manage.py test users
docker-compose exec web python manage.py test appointments

# С покрытием (требуется установить coverage)
docker-compose exec web poetry add coverage
docker-compose exec web coverage run manage.py test
docker-compose exec web coverage report
```

Структура тестов
```commandline
appointments/tests/
├── test_models.py          # Тесты моделей Appointment, DiagnosticResult
├── test_services.py        # Тесты генерации слотов, проверки доступности
├── test_views.py           # Тесты контроллеров (запись, список, детали)
├── test_business_rules.py  # Тесты бизнес-логики (статусы, валидации)
└── test_auth.py            # Тесты авторизации и прав доступа

users/tests/
├── test_models.py          # Тесты CustomUser, валидации полей
├── test_views.py           # Тесты регистрации, активации, входа
└── test_forms.py           # Тесты форм (валидация, очистка данных)
```

###### Пример теста бизнес-логики (appointments/tests/test_business_rules.py)
```commandline
from django.test import TestCase
from datetime import datetime, time
from appointments.services import get_available_slots
from appointments.models import Appointment
from users.models import CustomUser
from core.models import Doctor

class AppointmentBusinessRulesTest(TestCase):
    def test_slot_generation_respects_work_hours(self):
        """Слоты генерируются только в рабочие часы 9:00-18:00"""
        slots = generate_slots(datetime(2024, 1, 15).date())
        
        self.assertEqual(slots[0].time(), time(9, 0))
        self.assertLess(slots[-1].time(), time(18, 0))
        
    def test_busy_slots_excluded(self):
        """Занятые слоты исключаются из доступных"""
        doctor = Doctor.objects.create(...)
        Appointment.objects.create(
            doctor=doctor,
            date=datetime(2024, 1, 15, 10, 0)  # Занято 10:00
        )
        
        available = get_available_slots(doctor, datetime(2024, 1, 15).date())
        slot_10 = datetime(2024, 1, 15, 10, 0)
        
        self.assertNotIn(slot_10, available)
```

### 📧 Настройка email-уведомлений
Конфигурация SMTP (Mail.ru)
- В файле config/settings.py уже настроен SMTP-бэкенд:
```commandline
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@mail.ru'  # Замените на ваш
EMAIL_HOST_PASSWORD = os.getenv('PASSWORD_FOR_MAIL')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```
##### Получение пароля приложения для Mail.ru
1. Зайдите в Настройки безопасности Mail.ru
2. Включите Двухфакторную аутентификацию
3. Создайте Пароль для внешних приложений
4. Скопируйте пароль и укажите в .env

```commandline
PASSWORD_FOR_MAIL=abcd-efgh-ijkl-mnop
```

Тестирование отправки писем
```commandline
# Отправка тестового письма через Django shell
docker-compose exec web python manage.py shell
```
```commandline
from django.core.mail import send_mail
send_mail(
    subject='Тестовое письмо',
    message='Если вы видите это — настройка работает!',
    from_email=None,  # Использует DEFAULT_FROM_EMAIL
    recipient_list=['your-email@example.com'],
)
```
### 🔐 Переменные окружения
Полный список .env
```commandline
# === Django ===
SECRET_KEY=django-insecure-change-me-in-production
DEBUG=True  # False в продакшене!

# === PostgreSQL ===
POSTGRES_DB=medical_lab
POSTGRES_USER=medical_user
POSTGRES_PASSWORD=strong_password_here
POSTGRES_HOST=db  # 'localhost' при локальном запуске без Docker
POSTGRES_PORT=5432

# === Email (SMTP) ===
PASSWORD_FOR_MAIL=your-app-password-here

# === Опционально ===
# Дополнительные настройки можно добавить по необходимости
```

##### Безопасность
+ ❌ Никогда не коммитьте файл .env в репозиторий
+ ✅ Используйте .env.example или .env.sample как шаблон
+ ✅ В продакшене передавайте переменные через секреты (Docker secrets, Kubernetes ConfigMaps, etc.)

### 📄 Лицензия
Проект распространяется под лицензией MIT. Подробнее — в файле LICENSE.
##### 💡 Совет разработчику:
Перед началом работы убедитесь, что ваша локальная среда синхронизирована с feature/basic_settings. Регулярно делайте git pull и проверяйте миграции:
```commandline
git pull origin feature/basic_settings
docker-compose exec web python manage.py showmigrations
```

Документация актуальна на момент последнего коммита в ветке feature/basic_settings. При обновлении кода рекомендуется сверяться с изменениями в README.md. 