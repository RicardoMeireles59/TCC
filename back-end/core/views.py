from django.shortcuts import render, redirect
from .forms import RegisterForm

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # ou outra rota após cadastro
    else:
        form = RegisterForm()

    return render(request, "auth/register.html", {"form": form})