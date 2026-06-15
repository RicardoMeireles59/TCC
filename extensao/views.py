import re

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .forms import RegisterForm, LoginForm, FlashcardForm
from .models import CapturedSentence, Flashcard, Video
from .services.dashboard_service import get_dashboard_flashcards


# ── Sentence processing ──────────────────────────────────────────────────────

_SENTENCE_END = re.compile(r'(?<=[.!?])\s+')
_MIN_WORDS = 3


def _split_into_sentences(text: str) -> list[str]:
    """Split text on sentence boundaries; discard fragments shorter than _MIN_WORDS."""
    parts = _SENTENCE_END.split(text.strip())
    return [p.strip() for p in parts if len(p.strip().split()) >= _MIN_WORDS]


def _normalize(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip().lower()


# ── Web views (Django session auth) ─────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('flashcards-page')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('flashcards-page')
        error = 'Usuário ou senha incorretos.'

    return render(request, 'extensao/login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('login-page')


@login_required(login_url='/extensao/login/')
def flashcards_page(request):
    sentences = CapturedSentence.objects.filter(
        user=request.user, reviewed=False
    ).order_by('-captured_at')[:100]
    flashcards = Flashcard.objects.filter(user=request.user).order_by('-created_at')[:50]
    return render(request, 'extensao/flashcards.html', {
        'sentences': sentences,
        'flashcards': flashcards,
    })


# ── Web app views (dashboard/auth) — vindas do antigo back-end/core ───────────

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


@login_required
def dashboard_view(request):
    flashcards = get_dashboard_flashcards(request.user, request)
    paginator = Paginator(flashcards, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "dashboard/index.html", {"page_obj": page_obj})


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
    messages.success(request, "Progresso atualizado.")
    return redirect("dashboard")


@login_required
def flashcard_create(request):
    if request.method == "POST":
        form = FlashcardForm(request.POST)
        if form.is_valid():
            fc = form.save(commit=False)
            fc.user = request.user
            fc.save()
            messages.success(request, "Flashcard criado.")
            return redirect("dashboard")
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
            return redirect("dashboard")
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
    return redirect("dashboard")


# ── API views (Chrome extension — token auth) ────────────────────────────────

class CaptionReceiveView(APIView):
    """Receives EN+PT caption pairs from the Chrome extension, splits into sentences."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        en_raw = request.data.get('en', '').strip()
        pt_raw = request.data.get('pt', '').strip()
        video_id = request.data.get('video_id', '').strip()[:50]

        if not en_raw:
            return Response({'error': 'en é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)

        en_sentences = _split_into_sentences(en_raw) or [en_raw]
        pt_sentences = _split_into_sentences(pt_raw) if pt_raw else []

        created = 0
        for i, en_sent in enumerate(en_sentences):
            pt_sent = pt_sentences[i] if i < len(pt_sentences) else ''
            # Deduplicate: skip if this exact EN text already exists for this user+video
            exists = CapturedSentence.objects.filter(
                user=request.user,
                video_id=video_id,
                en=en_sent,
            ).exists()
            if not exists:
                CapturedSentence.objects.create(
                    user=request.user,
                    en=en_sent,
                    pt=pt_sent,
                    video_id=video_id,
                )
                created += 1

        return Response({'created': created}, status=status.HTTP_201_CREATED)


class SentenceView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = CapturedSentence.objects.filter(user=request.user, reviewed=False)
        video_id = request.GET.get('video_id')
        if video_id:
            qs = qs.filter(video_id=video_id)
        return Response(list(qs.values('id', 'en', 'pt', 'video_id', 'captured_at')))

    def patch(self, request, pk):
        try:
            sentence = CapturedSentence.objects.get(pk=pk, user=request.user)
        except CapturedSentence.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if 'reviewed' in request.data:
            sentence.reviewed = bool(request.data['reviewed'])
        if 'saved_as_flashcard' in request.data:
            sentence.saved_as_flashcard = bool(request.data['saved_as_flashcard'])
        sentence.save()
        return Response({'id': sentence.id, 'reviewed': sentence.reviewed})


class FlashcardView(APIView):
    """CRUD de Flashcard. Coleção (GET/POST) e detalhe (GET/PATCH/DELETE por pk)."""
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    FIELDS = ('id', 'phrase', 'translation', 'deck', 'status', 'progress', 'video', 'created_at')

    @staticmethod
    def _serialize(fc):
        return {
            'id': fc.id, 'phrase': fc.phrase, 'translation': fc.translation,
            'deck': fc.deck, 'status': fc.status, 'progress': fc.progress,
            'video': fc.video_id,
        }

    def _get_obj(self, request, pk):
        try:
            return Flashcard.objects.get(pk=pk, user=request.user)
        except Flashcard.DoesNotExist:
            return None

    def get(self, request, pk=None):
        if pk is not None:
            fc = self._get_obj(request, pk)
            if fc is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(self._serialize(fc))
        qs = Flashcard.objects.filter(user=request.user)
        deck = request.GET.get('deck')
        if deck:
            qs = qs.filter(deck=deck)
        return Response(list(qs.values(*self.FIELDS)))

    def post(self, request):
        phrase = request.data.get('phrase', '').strip()
        if not phrase:
            return Response({'error': 'phrase é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)

        fc = Flashcard.objects.create(
            user=request.user,
            phrase=phrase,
            translation=request.data.get('translation', '').strip(),
            deck=request.data.get('deck', 'geral'),
        )
        return Response(self._serialize(fc), status=status.HTTP_201_CREATED)

    def patch(self, request, pk=None):
        if pk is None:
            return Response({'error': 'pk obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
        fc = self._get_obj(request, pk)
        if fc is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        for field in ('phrase', 'translation', 'deck', 'status'):
            if field in request.data:
                setattr(fc, field, request.data[field])
        if 'progress' in request.data:
            try:
                fc.progress = int(request.data['progress'])
            except (TypeError, ValueError):
                return Response({'error': 'progress inválido'}, status=status.HTTP_400_BAD_REQUEST)
        fc.save()
        return Response(self._serialize(fc))

    def delete(self, request, pk=None):
        if pk is None:
            return Response({'error': 'pk obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
        fc = self._get_obj(request, pk)
        if fc is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        fc.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
