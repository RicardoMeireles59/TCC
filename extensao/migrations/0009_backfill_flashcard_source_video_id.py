from django.db import migrations


def backfill_source_video_id(apps, schema_editor):
    """Preenche source_video_id dos flashcards 'Do vídeo' já existentes.

    Casa cada flashcard sem id de vídeo com a frase capturada de origem
    (mesmo usuário + en == phrase) e copia o video_id dela.
    """
    Flashcard = apps.get_model('extensao', 'Flashcard')
    CapturedSentence = apps.get_model('extensao', 'CapturedSentence')

    pending = Flashcard.objects.filter(deck='video', source_video_id='')
    for fc in pending.iterator():
        sentence = (CapturedSentence.objects
                    .filter(user=fc.user, en=fc.phrase)
                    .exclude(video_id='')
                    .order_by('captured_at')
                    .first())
        if sentence:
            fc.source_video_id = sentence.video_id
            fc.save(update_fields=['source_video_id'])


class Migration(migrations.Migration):

    dependencies = [
        ('extensao', '0008_flashcard_source_video_id'),
    ]

    operations = [
        migrations.RunPython(backfill_source_video_id, migrations.RunPython.noop),
    ]
