from extensao.models import Flashcard


def get_dashboard_flashcards(user, request):
    flashcards = Flashcard.objects.select_related("video", "deck_obj").filter(user=user)

    # ==========================
    # SEARCH
    # ==========================
    search = request.GET.get("search")
    if search:
        flashcards = flashcards.filter(phrase__icontains=search)

    # ==========================
    # FILTER (status + baralho unificado)
    # ==========================
    filter_val = request.GET.get("filter")
    if filter_val:
        normalized_filter = filter_val.strip()
        if normalized_filter.startswith("status:"):
            status_value = normalized_filter.split(":", 1)[1].strip()
            if status_value in {"new", "learning", "reviewed"}:
                flashcards = flashcards.filter(status=status_value)
        elif normalized_filter in {"new", "learning", "reviewed"}:
            flashcards = flashcards.filter(status=normalized_filter)
        elif normalized_filter == "deck:all":
            flashcards = flashcards.filter(deck_obj__isnull=False)
        elif normalized_filter == "deck:none":
            flashcards = flashcards.filter(deck_obj__isnull=True)
        elif normalized_filter.startswith("deck:"):
            deck_id = normalized_filter.replace("deck:", "", 1)
            if deck_id.isdigit():
                flashcards = flashcards.filter(deck_obj_id=deck_id)

    # ==========================
    # ORDERING
    # ==========================
    ordering = request.GET.get("ordering")
    if ordering:
        flashcards = flashcards.order_by(ordering)

    return flashcards