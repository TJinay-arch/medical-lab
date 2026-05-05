from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "avatar", "phone_number", "username", "country")
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "Введите почту", "class": "form-control"}),
            "username": forms.TextInput(attrs={"placeholder": "Например: Ilya", "class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "+79991234567", "class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # avatar
        self.fields["avatar"].widget.attrs.update({"class": "form-control"})

        # 🔥 ВОТ ГЛАВНОЕ
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Введите пароль"})

        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Повторите пароль"})


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "Введите email"})

        self.fields["password"].widget.attrs.update({"class": "form-control", "placeholder": "Введите пароль"})
