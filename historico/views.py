from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


@login_required(login_url='/login/')
def historico_view(request):
    """Renderiza a página de histórico de estudos."""
    context = {
        'page_title': 'Histórico de Estudos',
    }
    return render(request, 'historico/index.html', context)


@login_required
@require_http_methods(["GET"])
def get_history_data(request):
    """API para retornar dados do histórico em JSON (mock para agora)."""
    
    # TODO: Conectar com modelo de banco de dados
    # Por enquanto, retorna dados mock
    
    mock_data = [
        {
            'date': '2026-06-10',
            'cardsStudied': 15,
            'correct': 12,
            'incorrect': 3,
            'duration': '12 min'
        },
        {
            'date': '2026-06-09',
            'cardsStudied': 20,
            'correct': 16,
            'incorrect': 4,
            'duration': '18 min'
        },
        {
            'date': '2026-06-08',
            'cardsStudied': 10,
            'correct': 9,
            'incorrect': 1,
            'duration': '8 min'
        },
        {
            'date': '2026-06-07',
            'cardsStudied': 25,
            'correct': 18,
            'incorrect': 7,
            'duration': '22 min'
        },
        {
            'date': '2026-06-06',
            'cardsStudied': 12,
            'correct': 10,
            'incorrect': 2,
            'duration': '10 min'
        },
        {
            'date': '2026-06-05',
            'cardsStudied': 18,
            'correct': 14,
            'incorrect': 4,
            'duration': '15 min'
        }
    ]
    
    return JsonResponse({
        'success': True,
        'data': mock_data
    })
