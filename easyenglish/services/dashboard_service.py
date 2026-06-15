from extensao.models import Flashcard


def get_dashboard_flashcards(user, request):
    flashcards = Flashcard.objects.select_related("video").filter(user=user)

    # ==========================
    # SEARCH
    # ==========================
    search = request.GET.get("search")
    if search:
        flashcards = flashcards.filter(phrase__icontains=search)

    # ==========================
    # STATUS FILTER
    # ==========================
    status = request.GET.get("status")
    if status:
        flashcards = flashcards.filter(status=status)

    # ==========================
    # DECK FILTER (origem)
    # ==========================
    deck = request.GET.get("deck")
    if deck:
        flashcards = flashcards.filter(deck=deck)

    # ==========================
    # ORDERING
    # ==========================
    ordering = request.GET.get("ordering")
    if ordering:
        flashcards = flashcards.order_by(ordering)

    return flashcards
