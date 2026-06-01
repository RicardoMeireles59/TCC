import requests as http_client
from django.conf import settings
from django.http import JsonResponse
from lingua import Language, LanguageDetectorBuilder
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Flashcard, Legenda

# Detector construído uma vez no carregamento do módulo (evita overhead por requisição)
_detector = LanguageDetectorBuilder.from_all_languages().build()

_LANG_MAP = {
    Language.ENGLISH:    'en',
    Language.PORTUGUESE: 'pt',
}

_LANG_NAMES = {
    'en': 'inglês',
    'pt': 'português',
}

MYMEMORY_URL = 'https://api.mymemory.translated.net/get'


def api_status(request):
    return JsonResponse({
        'status': 'ok',
        'endpoints': {
            'auth':       '/extensao/auth/token/',
            'traducao':   '/extensao/traducao/',
            'flashcards': '/extensao/flashcards/',
            'legendas':   '/extensao/legendas/',
        }
    })


def _detect_lang(text: str) -> str | None:
    """Retorna 'en', 'pt' ou None se não for nenhum dos dois ou indeterminado."""
    detected = _detector.detect_language_of(text)
    return _LANG_MAP.get(detected)


def _translate(text: str, source: str, target: str) -> str | None:
    """Chama MyMemory e retorna o texto traduzido, ou None em caso de erro."""
    params = {'q': text, 'langpair': f'{source}|{target}'}
    email = getattr(settings, 'MYMEMORY_EMAIL', '')
    if email:
        params['de'] = email
    try:
        resp = http_client.get(MYMEMORY_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get('responseStatus') == 200:
            return data['responseData']['translatedText']
    except Exception:
        pass
    return None


class TraducaoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        text = request.data.get('text', '').strip()
        if not text:
            return Response({'error': 'text é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)

        source = _detect_lang(text)
        if source is None:
            return Response(
                {
                    'error': 'unsupported_language',
                    'message': 'Por favor, digite a frase em inglês ou português.',
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        target = 'pt' if source == 'en' else 'en'
        translated = _translate(text, source, target)
        if translated is None:
            return Response(
                {'error': 'Falha ao conectar ao serviço de tradução. Tente novamente.'},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response({
            'original':    text,
            'translated':  translated,
            'source_lang': source,
            'target_lang': target,
        })


class FlashcardView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        deck = request.GET.get('deck')
        qs = Flashcard.objects.all()
        if deck:
            qs = qs.filter(deck=deck)
        return Response(list(qs.values('id', 'phrase', 'translation', 'deck', 'created_at')))

    def post(self, request):
        phrase = request.data.get('phrase', '').strip()
        if not phrase:
            return Response({'error': 'phrase é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)

        fc = Flashcard.objects.create(
            phrase=phrase,
            translation=request.data.get('translation', '').strip(),
            deck=request.data.get('deck', 'geral'),
        )
        return Response(
            {'id': fc.id, 'phrase': fc.phrase, 'translation': fc.translation, 'deck': fc.deck},
            status=status.HTTP_201_CREATED,
        )


class LegendaView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        video_id = request.GET.get('video_id')
        validada = request.GET.get('validada')
        qs = Legenda.objects.all()
        if video_id:
            qs = qs.filter(video_id=video_id)
        if validada is not None:
            qs = qs.filter(validada=validada.lower() == 'true')
        return Response(list(qs.values('id', 'en', 'pt', 'video_id', 'captured_at', 'validada')))

    def post(self, request):
        en = request.data.get('en', '').strip()
        if not en:
            return Response({'error': 'en é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)

        legenda = Legenda.objects.create(
            en=en,
            pt=request.data.get('pt', '').strip(),
            video_id=request.data.get('video_id', '').strip(),
        )
        return Response(
            {'id': legenda.id, 'en': legenda.en, 'pt': legenda.pt},
            status=status.HTTP_201_CREATED,
        )
