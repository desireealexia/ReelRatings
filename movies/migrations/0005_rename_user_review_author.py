# Generated by Django 5.1.5 on 2025-03-03 18:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_alter_review_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='user',
            new_name='author',
        ),
    ]
