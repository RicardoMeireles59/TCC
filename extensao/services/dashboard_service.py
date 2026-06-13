from extensao.models import StudyCard


def get_dashboard_flashcards(user, request):
    flashcards = StudyCard.objects.select_related("video").filter(user=user)

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
    # ORDERING
    # ==========================
    ordering = request.GET.get("ordering")
    if ordering:
        flashcards = flashcards.order_by(ordering)

    return flashcards
