"""Rotas do app web (auth + dashboard), montadas na raiz do projeto.

Vieram do antigo back-end/core. Os nomes (home/login/register/logout/dashboard/
update_flashcard_status) são preservados porque os templates os referenciam.
"""
from django.urls import path

from .views import (
    home_view,
    register_view,
    web_login_view,
    web_logout_view,
    dashboard_view,
    update_flashcard_status,
)

urlpatterns = [
    path("", home_view, name="home"),
    path("register/", register_view, name="register"),
    path("login/", web_login_view, name="login"),
    path("logout/", web_logout_view, name="logout"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path(
        "flashcard/<int:flashcard_id>/update/",
        update_flashcard_status,
        name="update_flashcard_status",
    ),
]
