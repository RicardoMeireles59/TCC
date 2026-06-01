from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full border rounded p-3"
        })
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full border rounded p-3"
        })
    )

    class Meta:
        model = User

        fields = [
            "username",
            "email",
            "password"
        ]

        widgets = {
            "username": forms.TextInput(attrs={
                "class": "w-full border rounded p-3"
            }),

            "email": forms.EmailInput(attrs={
                "class": "w-full border rounded p-3"
            }),
        }