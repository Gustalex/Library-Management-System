# Generated by Django 5.0.7 on 2024-07-19 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='id_genre',
            new_name='genre',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='book_status',
            new_name='status',
        ),
    ]
