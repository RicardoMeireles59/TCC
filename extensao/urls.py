from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import FlashcardView, LegendaView, TraducaoView, api_status

urlpatterns = [
    path('',            api_status,              name='extensao-status'),
    path('auth/token/', obtain_auth_token,       name='extensao-token'),
    path('traducao/',   TraducaoView.as_view(),  name='traducao'),
    path('flashcards/', FlashcardView.as_view(), name='flashcards'),
    path('legendas/',   LegendaView.as_view(),   name='legendas'),
]
