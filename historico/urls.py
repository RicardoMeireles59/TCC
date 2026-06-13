from django.urls import path
from .views import historico_view, get_history_data

app_name = 'historico'

urlpatterns = [
    path('', historico_view, name='index'),
    path('api/dados/', get_history_data, name='api_history_data'),
]
