# Generated by Django 5.1.5 on 2025-03-03 19:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_alter_review_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='author',
            new_name='user',
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('movie_id', 'user')},
        ),
    ]
