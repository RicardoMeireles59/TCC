from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Max
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST, require_http_methods

from extensao.models import CapturedSentence, Flashcard

from .forms import RegisterForm, LoginForm, FlashcardForm
from .models import EstudoSessao
from .services.dashboard_service import get_dashboard_flashcards


# ── Auth ──────────────────────────────────────────────────────────────────────

def home_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return redirect("login")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Conta criada com sucesso.")
            return redirect("login")
        messages.error(request, "Erro ao criar conta.")
    else:
        form = RegisterForm()
    return render(request, "auth/register.html", {"form": form})


def web_login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Login realizado com sucesso.")
            return redirect("dashboard")
        messages.error(request, "Usuário ou senha inválidos.")
    return render(request, "auth/login.html", {"form": form})


def web_logout_view(request):
    logout(request)
    messages.success(request, "Logout realizado com sucesso.")
    return redirect("login")


# ── Dashboard / flashcards ────────────────────────────────────────────────────

@login_required
def dashboard_view(request):
    """Visão geral (Início): contadores + vídeos recentes."""
    user = request.user
    cards = Flashcard.objects.filter(user=user)
    stats = {
        "revisar": cards.filter(status="new").count(),
        "aprendidos": cards.filter(status="reviewed").count(),
        "videos": (CapturedSentence.objects.filter(user=user)
                   .exclude(video_id="").values("video_id").distinct().count()),
    }
    recent_videos = list(
        CapturedSentence.objects.filter(user=user).exclude(video_id="")
        .values("video_id")
        .annotate(n=Count("id"), last=Max("captured_at"))
        .order_by("-last")[:5]
    )
    return render(request, "dashboard/index.html", {"stats": stats, "recent_videos": recent_videos})


@login_required
def flashcards_list_view(request):
    """Lista + CRUD dos flashcards do usuário."""
    flashcards = get_dashboard_flashcards(request.user, request)
    paginator = Paginator(flashcards, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "flashcards/list.html", {"page_obj": page_obj})


@login_required
def study_view(request):
    """Tela de estudo (flip-cards) com os flashcards do usuário."""
    cards = Flashcard.objects.filter(user=request.user)
    counts = {
        "acertos": cards.filter(status="reviewed").count(),
        "revisoes": cards.filter(status="learning").count(),
        "erros": cards.filter(status="new").count(),
    }
    return render(request, "flashcards/estudar.html", {"cards": cards, "counts": counts})


def _record_study_event(user, status_val):
    """Agrega o resultado de um card numa sessão de estudo diária do usuário."""
    hoje = timezone.localdate()
    sessao = EstudoSessao.objects.filter(user=user, data__date=hoje).first()
    if sessao is None:
        sessao = EstudoSessao.objects.create(user=user)
    sessao.cards_estudados += 1
    if status_val == "reviewed":      # Acertei
        sessao.acertos += 1
    elif status_val == "new":         # Errei
        sessao.erros += 1
    # "learning" (Revisar) conta como card estudado, sem acerto/erro
    decorrido = (timezone.now() - sessao.data).total_seconds() / 60
    sessao.duracao_minutos = max(sessao.duracao_minutos, int(decorrido))
    sessao.save()


@login_required
def update_flashcard_status(request, flashcard_id):
    flashcard = get_object_or_404(Flashcard, id=flashcard_id, user=request.user)
    status_val = request.POST.get("status")
    progress_val = request.POST.get("progress")
    if status_val:
        flashcard.status = status_val
    if progress_val:
        flashcard.progress = int(progress_val)
    flashcard.save()
    if request.POST.get("origem") == "study":
        if status_val:
            _record_study_event(request.user, status_val)
        return redirect("study")
    messages.success(request, "Progresso atualizado.")
    return redirect("flashcards_list")


@login_required
def flashcard_create(request):
    if request.method == "POST":
        form = FlashcardForm(request.POST)
        if form.is_valid():
            fc = form.save(commit=False)
            fc.user = request.user
            fc.save()
            messages.success(request, "Flashcard criado.")
            return redirect("flashcards_list")
        messages.error(request, "Verifique os dados do formulário.")
    else:
        form = FlashcardForm()
    return render(request, "dashboard/flashcard_form.html", {"form": form, "modo": "Novo"})


@login_required
def flashcard_edit(request, flashcard_id):
    flashcard = get_object_or_404(Flashcard, id=flashcard_id, user=request.user)
    if request.method == "POST":
        form = FlashcardForm(request.POST, instance=flashcard)
        if form.is_valid():
            form.save()
            messages.success(request, "Flashcard atualizado.")
            return redirect("flashcards_list")
        messages.error(request, "Verifique os dados do formulário.")
    else:
        form = FlashcardForm(instance=flashcard)
    return render(request, "dashboard/flashcard_form.html", {"form": form, "modo": "Editar"})


@login_required
@require_POST
def flashcard_delete(request, flashcard_id):
    flashcard = get_object_or_404(Flashcard, id=flashcard_id, user=request.user)
    flashcard.delete()
    messages.success(request, "Flashcard excluído.")
    return redirect("flashcards_list")


# ── Histórico de estudos ──────────────────────────────────────────────────────

@login_required(login_url='/login/')
def historico_view(request):
    """Renderiza a página de histórico de estudos."""
    return render(request, 'historico/index.html', {'page_title': 'Histórico de Estudos'})


@login_required
@require_http_methods(["GET"])
def get_history_data(request):
    """Retorna as sessões de estudo reais do usuário em JSON."""
    sessoes = EstudoSessao.objects.filter(user=request.user)  # Meta.ordering = -data
    data = [{
        "date": s.data.strftime("%Y-%m-%d"),
        "cardsStudied": s.cards_estudados,
        "correct": s.acertos,
        "incorrect": s.erros,
        "duration": f"{s.duracao_minutos} min",
    } for s in sessoes]
    return JsonResponse({"success": True, "data": data})
