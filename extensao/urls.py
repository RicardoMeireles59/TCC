from django.urls import path
from .views import FlashcardView, LegendaView, api_status

urlpatterns = [
    path('',            api_status,              name='extensao-status'),
    path('flashcards/', FlashcardView.as_view(), name='flashcards'),
    path('legendas/',   LegendaView.as_view(),   name='legendas'),
]
