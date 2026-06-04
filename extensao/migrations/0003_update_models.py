import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extensao', '0002_legenda'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Remove Legenda
        migrations.DeleteModel(name='Legenda'),

        # Add nullable user FK to existing Flashcard rows
        migrations.AddField(
            model_name='flashcard',
            name='user',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='flashcards',
                to=settings.AUTH_USER_MODEL,
            ),
        ),

        # Create CapturedSentence
        migrations.CreateModel(
            name='CapturedSentence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('en', models.TextField()),
                ('pt', models.TextField(blank=True)),
                ('video_id', models.CharField(blank=True, db_index=True, max_length=50)),
                ('captured_at', models.DateTimeField(auto_now_add=True)),
                ('reviewed', models.BooleanField(default=False)),
                ('saved_as_flashcard', models.BooleanField(default=False)),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='sentences',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={'ordering': ['-captured_at']},
        ),
    ]
