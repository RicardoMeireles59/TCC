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
        if filter_val.startswith("status:"):
            flashcards = flashcards.filter(status=filter_val.replace("status:", ""))
        elif filter_val == "deck:none":
            flashcards = flashcards.filter(deck_obj__isnull=True)
        elif filter_val.startswith("deck:"):
            flashcards = flashcards.filter(deck_obj_id=filter_val.replace("deck:", ""))
        elif filter_val == "deck:all":
            flashcards = flashcards.filter(deck_obj__isnull=False)

    # ==========================
    # ORDERING
    # ==========================
    ordering = request.GET.get("ordering")
    if ordering:
        flashcards = flashcards.order_by(ordering)

    return flashcards