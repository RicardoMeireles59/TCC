from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib import messages

from django.contrib.auth import (
    login,
    logout
)

from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

from .forms import (
    RegisterForm,
    LoginForm
)

from .models import Flashcard

from .services.dashboard_service import (
    get_dashboard_flashcards
)


# ==========================================
# AUTH
# ==========================================

def register_view(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            messages.success(
                request,
                "Conta criada com sucesso."
            )

            return redirect("login")

        messages.error(
            request,
            "Erro ao criar conta."
        )

    else:
        form = RegisterForm()

    return render(
        request,
        "auth/register.html",
        {
            "form": form
        }
    )


def home_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return redirect("login")


def login_view(request):

    form = LoginForm(
        request,
        data=request.POST or None
    )

    if request.method == "POST":

        if form.is_valid():

            login(
                request,
                form.get_user()
            )

            messages.success(
                request,
                "Login realizado com sucesso."
            )

            return redirect("dashboard")

        messages.error(
            request,
            "Usuário ou senha inválidos."
        )

    return render(
        request,
        "auth/login.html",
        {
            "form": form
        }
    )


def logout_view(request):

    logout(request)

    messages.success(
        request,
        "Logout realizado com sucesso."
    )

    return redirect("login")


# ==========================================
# DASHBOARD
# ==========================================

@login_required
def dashboard_view(request):

    flashcards = get_dashboard_flashcards(
        request.user,
        request
    )

    paginator = Paginator(
        flashcards,
        10
    )

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(
        page_number
    )

    return render(
        request,
        "dashboard/index.html",
        {
            "page_obj": page_obj
        }
    )


# ==========================================
# FLASHCARDS
# ==========================================

@login_required
def update_flashcard_status(
    request,
    flashcard_id
):

    flashcard = get_object_or_404(
        Flashcard,
        id=flashcard_id,
        user=request.user
    )

    status = request.POST.get("status")

    progress = request.POST.get("progress")

    if status:
        flashcard.status = status

    if progress:
        flashcard.progress = int(progress)

    flashcard.save()

    messages.success(
        request,
        "Progresso atualizado."
    )

    return redirect("dashboard")