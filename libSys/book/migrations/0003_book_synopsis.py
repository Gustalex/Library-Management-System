# Generated by Django 5.0.7 on 2024-07-23 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_rename_id_genre_book_genre_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='synopsis',
            field=models.TextField(blank=True, null=True),
        ),
    ]
