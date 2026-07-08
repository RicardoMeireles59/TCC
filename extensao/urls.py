from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import CaptionReceiveView, DeckView, SentenceView, FlashcardView

urlpatterns = [
    # ── API (Chrome extension — token auth) ───────────────────────────────────
    path('api/token/',             obtain_auth_token,            name='api-token'),
    path('api/captions/',          CaptionReceiveView.as_view(), name='api-captions'),
    path('api/sentences/',         SentenceView.as_view(),       name='api-sentences'),
    path('api/sentences/<int:pk>/', SentenceView.as_view(),      name='api-sentence-detail'),
    path('api/flashcards/',         FlashcardView.as_view(),     name='api-flashcards'),
    path('api/flashcards/<int:pk>/', FlashcardView.as_view(),    name='api-flashcard-detail'),
    path('api/decks/',              DeckView.as_view(),          name='api-decks'),
]
