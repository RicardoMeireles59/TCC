from django.db import models
from django.contrib.auth.models import User


class CapturedSentence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sentences')
    en = models.TextField()
    pt = models.TextField(blank=True)
    video_id = models.CharField(max_length=50, blank=True, db_index=True)
    captured_at = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)
    saved_as_flashcard = models.BooleanField(default=False)

    class Meta:
        ordering = ['-captured_at']

    def __str__(self):
        return self.en[:60]


class Flashcard(models.Model):
    DECK_CHOICES = [
        ('geral',   'Geral'),
        ('frases',  'Frases do dia a dia'),
        ('phrasal', 'Phrasal Verbs'),
        ('vocab',   'Vocabulário'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='flashcards',
                             null=True, blank=True)
    phrase = models.TextField()
    translation = models.TextField(blank=True)
    deck = models.CharField(max_length=30, choices=DECK_CHOICES, default='geral')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.phrase[:60]


# ── Web app (dashboard) — vindos do antigo back-end/core ──────────────────────

class Video(models.Model):
    title = models.CharField(max_length=255)
    youtube_id = models.CharField(max_length=100, unique=True)
    thumbnail = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class StudyCard(models.Model):
    """Flashcard do app web (dashboard). Antes era core.Flashcard.

    Mantido separado do Flashcard da extensão (phrase/translation/deck), que
    serve ao fluxo de captura. Aqui o conteúdo é EN/PT vinculado a um vídeo,
    com status e progresso de estudo.
    """
    STATUS_CHOICES = (
        ("new", "Novo"),
        ("learning", "Aprendendo"),
        ("reviewed", "Revisado"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    english_text = models.TextField()
    portuguese_text = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    progress = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.english_text[:50]
