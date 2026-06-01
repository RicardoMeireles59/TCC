from django.shortcuts import render
from .forms import RegisterForm


def register_view(request):
    form = RegisterForm()

    return render(
        request,
        "auth/register.html",
        {
            "form": form
        }
    )