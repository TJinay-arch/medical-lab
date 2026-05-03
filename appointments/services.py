from datetime import datetime, timedelta, time
from .models import Appointment

WORK_START = time(9, 0)
WORK_END = time(18, 0)
SLOT_DURATION = 30  # минут


def generate_slots(date):
    start = datetime.combine(date, WORK_START)
    end = datetime.combine(date, WORK_END)

    slots = []
    current = start

    while current < end:
        slots.append(current)
        current += timedelta(minutes=SLOT_DURATION)

    return slots


def get_available_slots(doctor, date):
    slots = generate_slots(date)

    busy = Appointment.objects.filter(
        doctor=doctor,
        date__date=date
    ).values_list("date", flat=True)

    available = [slot for slot in slots if slot not in busy]

    return available
