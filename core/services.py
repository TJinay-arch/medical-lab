from .models import Notification


def notify(user, text):
    Notification.objects.create(user=user, text=text)
