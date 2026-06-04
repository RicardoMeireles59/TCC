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
