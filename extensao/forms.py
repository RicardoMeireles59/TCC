from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


User = get_user_model()


# ==================================================
# REGISTER FORM
# ==================================================

class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(
            attrs={"class": "w-full border rounded p-3"}
        )
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "w-full border rounded p-3"}
        )
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "w-full border rounded p-3", "placeholder": "Usuário"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "w-full border rounded p-3", "placeholder": "Email"}
            ),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "As senhas não coincidem.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


# ==================================================
# LOGIN FORM
# ==================================================

class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "w-full border rounded p-3", "placeholder": "Usuário"}
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "w-full border rounded p-3", "placeholder": "Senha"}
        )
    )
