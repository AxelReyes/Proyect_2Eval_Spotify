# Generated by Django 5.0.3 on 2024-06-02 21:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HeroSound', '0003_playlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playlist',
            old_name='usuario',
            new_name='user',
        ),
    ]
