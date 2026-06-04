from django.urls import path
from .views import (
    register_view,
    login_view,
    logout_view,
    dashboard_view,
    update_flashcard_status
)

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    path("dashboard/", dashboard_view, name="dashboard"),

    path(
        "flashcard/<int:flashcard_id>/update/",
        update_flashcard_status,
        name="update_flashcard_status"
    ),
]