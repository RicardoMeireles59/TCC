from core.models import Flashcard


def get_dashboard_flashcards(user, request):
    flashcards = Flashcard.objects.select_related("video", "theme").filter(user=user)

    # ========================== 
    # SEARCH
    # ==========================
    search = request.GET.get("search")
    if search:
        flashcards = flashcards.filter(english_text__icontains=search)

    # ==========================
    # STATUS FILTER
    # ==========================
    status = request.GET.get("status")
    if status:
        flashcards = flashcards.filter(status=status)

    # ==========================
    # THEME FILTER
    # ==========================
    theme = request.GET.get("theme")
    if theme:
        flashcards = flashcards.filter(theme__id=theme)

    # ==========================
    # ORDERING
    # ==========================
    ordering = request.GET.get("ordering")
    if ordering:
        flashcards = flashcards.order_by(ordering)

    return flashcards