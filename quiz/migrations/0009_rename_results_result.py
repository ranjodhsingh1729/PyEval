# Generated by Django 5.0.4 on 2024-04-16 16:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0008_alter_submission_source_lang'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Results',
            new_name='Result',
        ),
    ]
