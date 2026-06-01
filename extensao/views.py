import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Flashcard, Legenda


def api_status(request):
    return JsonResponse({
        'status': 'ok',
        'endpoints': {
            'flashcards': '/extensao/flashcards/',
            'legendas':   '/extensao/legendas/',
        }
    })


@method_decorator(csrf_exempt, name='dispatch')
class FlashcardView(View):

    def get(self, request):
        deck = request.GET.get('deck')
        qs = Flashcard.objects.all()
        if deck:
            qs = qs.filter(deck=deck)
        return JsonResponse(list(qs.values('id', 'phrase', 'translation', 'deck', 'created_at')), safe=False)

    def post(self, request):
        try:
            body = json.loads(request.body)
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({'error': 'JSON inválido'}, status=400)

        phrase = body.get('phrase', '').strip()
        if not phrase:
            return JsonResponse({'error': 'phrase é obrigatório'}, status=400)

        fc = Flashcard.objects.create(
            phrase=phrase,
            translation=body.get('translation', '').strip(),
            deck=body.get('deck', 'geral'),
        )
        return JsonResponse({'id': fc.id, 'phrase': fc.phrase, 'translation': fc.translation, 'deck': fc.deck}, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class LegendaView(View):

    def get(self, request):
        video_id = request.GET.get('video_id')
        validada = request.GET.get('validada')
        qs = Legenda.objects.all()
        if video_id:
            qs = qs.filter(video_id=video_id)
        if validada is not None:
            qs = qs.filter(validada=validada.lower() == 'true')
        return JsonResponse(list(qs.values('id', 'en', 'pt', 'video_id', 'captured_at', 'validada')), safe=False)

    def post(self, request):
        try:
            body = json.loads(request.body)
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({'error': 'JSON inválido'}, status=400)

        en = body.get('en', '').strip()
        if not en:
            return JsonResponse({'error': 'en é obrigatório'}, status=400)

        legenda = Legenda.objects.create(
            en=en,
            pt=body.get('pt', '').strip(),
            video_id=body.get('video_id', '').strip(),
        )
        return JsonResponse({'id': legenda.id, 'en': legenda.en, 'pt': legenda.pt}, status=201)
