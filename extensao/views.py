import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import CapturedSentence, Flashcard


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
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        deck = request.GET.get('deck')
        qs = Flashcard.objects.filter(user=request.user)
        if deck:
            qs = qs.filter(deck=deck)
        return Response(list(qs.values('id', 'phrase', 'translation', 'deck', 'created_at')))

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
        return Response(
            {'id': fc.id, 'phrase': fc.phrase, 'translation': fc.translation, 'deck': fc.deck},
            status=status.HTTP_201_CREATED,
        )
