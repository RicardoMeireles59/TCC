from django.contrib import admin
from .models import CapturedSentence, Deck, Flashcard, Video


@admin.register(CapturedSentence)
class CapturedSentenceAdmin(admin.ModelAdmin):
    list_display = ('en', 'pt', 'video_title', 'video_id', 'user', 'reviewed', 'captured_at')
    list_filter = ('reviewed', 'saved_as_flashcard', 'user')
    search_fields = ('en', 'pt', 'video_id', 'video_title')
    readonly_fields = ('captured_at',)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'youtube_id', 'created_at')
    search_fields = ('title', 'youtube_id')
    readonly_fields = ('created_at',)

@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'color', 'total_cards', 'created_at')
    list_filter = ('user',)
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)

    @admin.display(description='Qtd. cards')
    def total_cards(self, obj):
        return obj.cards.count()

@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ('phrase', 'translation', 'deck_obj', 'deck', 'status', 'progress', 'user', 'created_at')
    list_filter = ('deck_obj', 'deck', 'status', 'user')
    search_fields = ('phrase', 'translation')
    readonly_fields = ('created_at',)
