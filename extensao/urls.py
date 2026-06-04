from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    login_view, logout_view, flashcards_page,
    CaptionReceiveView, SentenceView, FlashcardView,
)

urlpatterns = [
    # ── Web (session auth) ────────────────────────────────────────────────────
    path('login/',      login_view,      name='login-page'),
    path('logout/',     logout_view,     name='logout'),
    path('flashcards/', flashcards_page, name='flashcards-page'),

    # ── API (Chrome extension — token auth) ───────────────────────────────────
    path('api/token/',             obtain_auth_token,            name='api-token'),
    path('api/captions/',          CaptionReceiveView.as_view(), name='api-captions'),
    path('api/sentences/',         SentenceView.as_view(),       name='api-sentences'),
    path('api/sentences/<int:pk>/', SentenceView.as_view(),      name='api-sentence-detail'),
    path('api/flashcards/',        FlashcardView.as_view(),      name='api-flashcards'),
]
