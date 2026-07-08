import re

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import CapturedSentence, Deck, Flashcard

# ── Sentence processing ──────────────────────────────────────────────────────

_SENTENCE_END = re.compile(r'(?<=[.!?])\s+')
_MIN_WORDS = 3


def _split_into_sentences(text: str) -> list[str]:
    """Split text on sentence boundaries; discard fragments shorter than _MIN_WORDS."""
    parts = _SENTENCE_END.split(text.strip())
    return [p.strip() for p in parts if len(p.strip().split()) >= _MIN_WORDS]


def _normalize(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip().lower()


# ── API views (Chrome extension — token auth) ────────────────────────────────

class CaptionReceiveView(APIView):
    """Receives EN+PT caption pairs from the Chrome extension, splits into sentences."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        en_raw = request.data.get('en', '').strip()
        pt_raw = request.data.get('pt', '').strip()
        video_id = request.data.get('video_id', '').strip()[:50]
        video_url = request.data.get('video_url', '').strip()[:500]
        video_title = request.data.get('video_title', '').strip()[:255]

        if not en_raw:
            return Response({'error': 'en é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)

        # Fallback: monta a URL canônica do YouTube a partir do id, caso a extensão
        # não a tenha enviado.
        if not video_url and video_id:
            video_url = f'https://www.youtube.com/watch?v={video_id}'

        en_sentences = _split_into_sentences(en_raw) or [en_raw]
        pt_sentences = _split_into_sentences(pt_raw) if pt_raw else []

        created = 0
        deck_obj = None  # criado sob demanda, só se houver flashcard novo
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
                    video_url=video_url,
                    video_title=video_title,
                    saved_as_flashcard=True,
                )
                # Toda frase capturada vira um flashcard estudável, associado a um
                # baralho real com o nome do vídeo (criado na primeira captura).
                if deck_obj is None:
                    deck_obj, _ = Deck.objects.get_or_create(
                        user=request.user,
                        name=(video_title or 'Do vídeo')[:100],
                    )
                Flashcard.objects.create(
                    user=request.user,
                    phrase=en_sent,
                    translation=pt_sent,
                    deck='video',
                    deck_obj=deck_obj,
                    source_video_id=video_id,
                    video_url=video_url,
                    video_title=video_title,
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


class DeckView(APIView):
    """Lista os baralhos do usuário (usado pelo popup da extensão)."""
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        decks = Deck.objects.filter(user=request.user)
        return Response([
            {'id': d.id, 'name': d.name, 'color': d.color}
            for d in decks
        ])


class FlashcardView(APIView):
    """CRUD de Flashcard. Coleção (GET/POST) e detalhe (GET/PATCH/DELETE por pk)."""
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def _serialize(fc):
        return {
            'id': fc.id, 'phrase': fc.phrase, 'translation': fc.translation,
            'deck': fc.deck, 'status': fc.status, 'progress': fc.progress,
            'deck_id': fc.deck_obj_id,
            'deck_name': fc.deck_obj.name if fc.deck_obj else None,
            'video': fc.video_id,
            'source_video_id': fc.source_video_id,
            'video_url': fc.video_url, 'video_title': fc.video_title,
            'created_at': fc.created_at,
        }

    def _get_obj(self, request, pk):
        try:
            return Flashcard.objects.get(pk=pk, user=request.user)
        except Flashcard.DoesNotExist:
            return None

    def _resolve_deck(self, request, deck_id):
        """Retorna (deck, error_response). deck_id vazio/None significa 'sem baralho'."""
        if deck_id in (None, '', 0):
            return None, None
        try:
            return Deck.objects.get(id=int(deck_id), user=request.user), None
        except (TypeError, ValueError, Deck.DoesNotExist):
            return None, Response({'error': 'deck_id inválido'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        if pk is not None:
            fc = self._get_obj(request, pk)
            if fc is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(self._serialize(fc))
        qs = Flashcard.objects.filter(user=request.user).select_related('deck_obj')
        deck = request.GET.get('deck')
        if deck:
            qs = qs.filter(deck=deck)
        deck_id = request.GET.get('deck_id')
        if deck_id and deck_id.isdigit():
            qs = qs.filter(deck_obj_id=deck_id)
        return Response([self._serialize(fc) for fc in qs])

    def post(self, request):
        phrase = request.data.get('phrase', '').strip()
        if not phrase:
            return Response({'error': 'phrase é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)

        deck_obj, err = self._resolve_deck(request, request.data.get('deck_id'))
        if err:
            return err

        fc = Flashcard.objects.create(
            user=request.user,
            phrase=phrase,
            translation=request.data.get('translation', '').strip(),
            deck=request.data.get('deck', 'geral'),
            deck_obj=deck_obj,
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
        if 'deck_id' in request.data:
            deck_obj, err = self._resolve_deck(request, request.data['deck_id'])
            if err:
                return err
            fc.deck_obj = deck_obj
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
