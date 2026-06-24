from django.db import migrations


def backfill_video_title_url(apps, schema_editor):
    """Preenche video_title/video_url dos flashcards 'Do vídeo' já existentes.

    Casa cada flashcard com uma frase capturada do mesmo vídeo (mesmo usuário +
    video_id == source_video_id), preferindo uma que já tenha título, e copia
    título/URL. Se não houver URL, monta a canônica a partir do id.
    """
    Flashcard = apps.get_model('extensao', 'Flashcard')
    CapturedSentence = apps.get_model('extensao', 'CapturedSentence')

    pending = Flashcard.objects.exclude(source_video_id='').filter(video_title='')
    for fc in pending.iterator():
        sentence = (CapturedSentence.objects
                    .filter(user=fc.user, video_id=fc.source_video_id)
                    .exclude(video_title='')
                    .order_by('captured_at')
                    .first())
        fc.video_title = sentence.video_title if sentence else ''
        fc.video_url = (
            (sentence.video_url if sentence and sentence.video_url else '')
            or f'https://www.youtube.com/watch?v={fc.source_video_id}'
        )
        fc.save(update_fields=['video_title', 'video_url'])


class Migration(migrations.Migration):

    dependencies = [
        ('extensao', '0011_flashcard_video_title_flashcard_video_url'),
    ]

    operations = [
        migrations.RunPython(backfill_video_title_url, migrations.RunPython.noop),
    ]
