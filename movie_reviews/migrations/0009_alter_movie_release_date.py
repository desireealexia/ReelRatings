# Generated by Django 5.1.5 on 2025-02-18 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_reviews', '0008_alter_movie_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='release_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
