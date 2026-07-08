"""Associa flashcards antigos (deck_obj vazio) a baralhos reais.

Cards vindos de vídeo entram num baralho com o nome do vídeo; os demais entram
num baralho com o rótulo do deck legado (Geral, Vocabulário, ...).
"""
from django.db import migrations

DECK_LABELS = {
    'geral':   'Geral',
    'frases':  'Frases do dia a dia',
    'phrasal': 'Phrasal Verbs',
    'vocab':   'Vocabulário',
    'video':   'Do vídeo',
}


def forwards(apps, schema_editor):
    Flashcard = apps.get_model('extensao', 'Flashcard')
    Deck = apps.get_model('extensao', 'Deck')
    qs = Flashcard.objects.filter(deck_obj__isnull=True, user__isnull=False)
    for fc in qs.iterator():
        name = (fc.video_title or DECK_LABELS.get(fc.deck, 'Geral'))[:100]
        deck, _ = Deck.objects.get_or_create(user_id=fc.user_id, name=name)
        fc.deck_obj = deck
        fc.save(update_fields=['deck_obj'])


class Migration(migrations.Migration):

    dependencies = [
        ('extensao', '0013_merge_20260701_0025'),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
