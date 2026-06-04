from extensao.models import Flashcard


def get_dashboard_flashcards(user, request):
    flashcards = Flashcard.objects.select_related("video").filter(user=user)

    search = request.GET.get("search")
    status = request.GET.get("status")
    ordering = request.GET.get("ordering")

    if search:
        flashcards = flashcards.filter(
            english_text__icontains=search
        )

    if status:
        flashcards = flashcards.filter(status=status)

    if ordering:
        flashcards = flashcards.order_by(ordering)

    return flashcards