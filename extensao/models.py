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


class Video(models.Model):
    title = models.CharField(max_length=255)
    youtube_id = models.CharField(max_length=100, unique=True)
    thumbnail = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Flashcard(models.Model):
    """Modelo único de flashcard.

    Unifica o antigo StudyCard: além de frase/tradução/baralho (criados a partir
    das legendas capturadas), guarda vínculo opcional com o vídeo de origem e o
    progresso de estudo (status/progress). O baralho (deck) identifica a origem.
    """
    DECK_CHOICES = [
        ('geral',   'Geral'),
        ('frases',  'Frases do dia a dia'),
        ('phrasal', 'Phrasal Verbs'),
        ('vocab',   'Vocabulário'),
        ('video',   'Do vídeo'),
    ]

    STATUS_CHOICES = (
        ('new',      'Novo'),
        ('learning', 'Aprendendo'),
        ('reviewed', 'Revisado'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='flashcards',
                             null=True, blank=True)
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, related_name='flashcards',
                              null=True, blank=True)
    source_video_id = models.CharField(max_length=50, blank=True)  # id do vídeo de origem (YouTube)
    phrase = models.TextField()                       # EN
    translation = models.TextField(blank=True)        # PT
    deck = models.CharField(max_length=30, choices=DECK_CHOICES, default='geral')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    progress = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.phrase[:60]
