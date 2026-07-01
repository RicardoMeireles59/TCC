from django.db import models
from django.contrib.auth.models import User


class CapturedSentence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sentences')
    en = models.TextField()
    pt = models.TextField(blank=True)
    video_id = models.CharField(max_length=50, blank=True, db_index=True)
    video_url = models.URLField(max_length=500, blank=True)
    video_title = models.CharField(max_length=255, blank=True)
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

class Deck(models.Model):
    """Baralho de flashcards criado pelo usuário."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='decks')
    name = models.CharField(max_length=100, verbose_name='Nome')
    description = models.TextField(blank=True, verbose_name='Descrição')
    color = models.CharField(max_length=7, default='#6366f1', verbose_name='Cor')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        unique_together = [['user', 'name']]
        verbose_name = 'Baralho'
        verbose_name_plural = 'Baralhos'

    def __str__(self):
        return self.name
    
class Flashcard(models.Model):
    """Modelo único de flashcard.

    Unifica o antigo StudyCard: além de frase/tradução/baralho (criados a partir
    das legendas capturadas), guarda vínculo opcional com o vídeo de origem e o
    progresso de estudo (status/progress). O baralho (deck) identifica a origem.
    """

    deck_obj = models.ForeignKey(
    'Deck',
    on_delete=models.SET_NULL,
    null=True, blank=True,
    related_name='cards',
    verbose_name='Baralho',
    )
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
    video_url = models.URLField(max_length=500, blank=True)        # link do vídeo de origem
    video_title = models.CharField(max_length=255, blank=True)     # título do vídeo de origem
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
    
    @property
    def deck_label(self):
        if self.deck_obj:
            return self.deck_obj.name
        return self.get_deck_display()
