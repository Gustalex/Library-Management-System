# Generated by Django 5.0.7 on 2024-07-23 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_book_synopsis'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='edition',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]