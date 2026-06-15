"""Rotas do app web (auth + dashboard + CRUD de flashcards), montadas na raiz.

Os nomes (home/login/register/logout/dashboard/...) são preservados porque os
templates os referenciam.
"""
from django.urls import path

from .views import (
    home_view,
    register_view,
    web_login_view,
    web_logout_view,
    dashboard_view,
    update_flashcard_status,
    flashcard_create,
    flashcard_edit,
    flashcard_delete,
)

urlpatterns = [
    path("", home_view, name="home"),
    path("register/", register_view, name="register"),
    path("login/", web_login_view, name="login"),
    path("logout/", web_logout_view, name="logout"),
    path("dashboard/", dashboard_view, name="dashboard"),

    # CRUD de flashcards (web)
    path("flashcard/novo/", flashcard_create, name="flashcard_create"),
    path("flashcard/<int:flashcard_id>/editar/", flashcard_edit, name="flashcard_edit"),
    path("flashcard/<int:flashcard_id>/excluir/", flashcard_delete, name="flashcard_delete"),
    path("flashcard/<int:flashcard_id>/update/", update_flashcard_status, name="update_flashcard_status"),
]
