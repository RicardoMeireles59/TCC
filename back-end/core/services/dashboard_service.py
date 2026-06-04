from extensao.models import Flashcard


def get_dashboard_flashcards(user, request):
    flashcards = Flashcard.objects.filter(user=user)

    search = request.GET.get("search")
    deck = request.GET.get("deck")
    ordering = request.GET.get("ordering")

    if search:
        flashcards = flashcards.filter(
            phrase__icontains=search
        )

    if deck:
        flashcards = flashcards.filter(deck=deck)

    if ordering:
        flashcards = flashcards.order_by(ordering)

    return flashcards