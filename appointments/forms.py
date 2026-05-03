from django import forms
from .models import Appointment, DiagnosticResult
from core.models import Doctor
from services.models import Service


class AppointmentForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )

    time = forms.CharField(required=False)

    class Meta:
        model = Appointment
        fields = ["doctor", "service", "date", "comment"]

        widgets = {
            "doctor": forms.Select(attrs={"class": "form-control"}),
            "service": forms.Select(attrs={"class": "form-control"}),
            "date": forms.DateTimeInput(attrs={
                "type": "datetime-local",
                "class": "form-control"
            }),
            "comment": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),
        }

    def __init__(self, *args, **kwargs):
        doctor_id = kwargs.pop("doctor_id", None)
        service_id = kwargs.pop("service_id", None)

        super().__init__(*args, **kwargs)

        # 🔥 ЕСЛИ ВЫБРАН ВРАЧ
        if doctor_id:
            doctor = Doctor.objects.get(id=doctor_id)

            # фиксируем врача
            self.fields["doctor"].initial = doctor
            self.fields["doctor"].disabled = True

            # фильтруем услуги
            self.fields["service"].queryset = doctor.services.all()

        # 🔥 ЕСЛИ ВЫБРАНА УСЛУГА
        if service_id:
            service = Service.objects.get(id=service_id)

            # фиксируем услугу
            self.fields["service"].initial = service
            self.fields["service"].disabled = True

            # фильтруем врачей
            self.fields["doctor"].queryset = service.doctors.all()


class DiagnosticResultForm(forms.ModelForm):
    class Meta:
        model = DiagnosticResult
        fields = ["text", "file"]

        widgets = {
            "text": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Введите заключение врача..."
            }),
            "file": forms.ClearableFileInput(attrs={
                "class": "form-control"
            })
        }
