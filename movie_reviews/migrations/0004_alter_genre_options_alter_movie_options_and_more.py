# Generated by Django 5.1.5 on 2025-02-17 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie_reviews', '0003_rename_password_hash_user_password'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='movie',
            options={'ordering': ['average_rating', '-release_date']},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-date_joined']},
        ),
        migrations.AlterModelOptions(
            name='watchlist',
            options={'ordering': ['-added_at']},
        ),
    ]
