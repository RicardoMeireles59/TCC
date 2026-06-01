from django.db import models


class Flashcard(models.Model):
    DECK_CHOICES = [
        ('geral',   'Geral'),
        ('frases',  'Frases do dia a dia'),
        ('phrasal', 'Phrasal Verbs'),
        ('vocab',   'Vocabulário'),
    ]

    phrase      = models.TextField()
    translation = models.TextField(blank=True)
    deck        = models.CharField(max_length=30, choices=DECK_CHOICES, default='geral')
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.phrase[:60]


class Legenda(models.Model):
    en          = models.TextField()
    pt          = models.TextField(blank=True)
    video_id    = models.CharField(max_length=20, blank=True, db_index=True)
    captured_at = models.DateTimeField(auto_now_add=True)
    validada    = models.BooleanField(default=False)

    class Meta:
        ordering = ['-captured_at']

    def __str__(self):
        return self.en[:60]
