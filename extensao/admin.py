from django.contrib import admin
from .models import CapturedSentence, Flashcard


@admin.register(CapturedSentence)
class CapturedSentenceAdmin(admin.ModelAdmin):
    list_display = ('en', 'pt', 'video_id', 'user', 'reviewed', 'captured_at')
    list_filter = ('reviewed', 'saved_as_flashcard', 'user')
    search_fields = ('en', 'pt', 'video_id')
    readonly_fields = ('captured_at',)


@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ('phrase', 'translation', 'deck', 'user', 'created_at')
    list_filter = ('deck', 'user')
    search_fields = ('phrase', 'translation')
    readonly_fields = ('created_at',)
