"""Rotas do app web (auth + dashboard + flashcards + histórico), montadas na raiz."""
from django.urls import path

from .views import (
    home_view,
    register_view,
    web_login_view,
    web_logout_view,
    dashboard_view,
    flashcards_list_view,
    study_view,
    update_flashcard_status,
    flashcard_create,
    flashcard_edit,
    flashcard_delete,
    historico_view,
    get_history_data,
    decks_list_view,   
    deck_create,       
    deck_edit,         
    deck_delete,       
)

urlpatterns = [
    path("", home_view, name="home"),
    path("register/", register_view, name="register"),
    path("login/", web_login_view, name="login"),
    path("logout/", web_logout_view, name="logout"),
    path("dashboard/", dashboard_view, name="dashboard"),

    # Flashcards (lista + estudo + CRUD)
    path("flashcards/", flashcards_list_view, name="flashcards_list"),
    path("estudar/", study_view, name="study"),
    path("flashcard/novo/", flashcard_create, name="flashcard_create"),
    path("flashcard/<int:flashcard_id>/editar/", flashcard_edit, name="flashcard_edit"),
    path("flashcard/<int:flashcard_id>/excluir/", flashcard_delete, name="flashcard_delete"),
    path("flashcard/<int:flashcard_id>/update/", update_flashcard_status, name="update_flashcard_status"),

    # Baralhos (CRUD)
    path("baralhos/", decks_list_view, name="decks_list"),
    path("baralho/novo/", deck_create, name="deck_create"),
    path("baralho/<int:deck_id>/editar/", deck_edit, name="deck_edit"),
    path("baralho/<int:deck_id>/excluir/", deck_delete, name="deck_delete"),

    # Histórico de estudos
    path("historico/", historico_view, name="historico"),
    path("historico/api/dados/", get_history_data, name="historico_api"),
]
