# Generated by Django 5.0.1 on 2024-04-07 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='token',
            field=models.CharField(default='1b1936fc-780e-4996-841a-4c6ed2534b5c', max_length=255),
            preserve_default=False,
        ),
    ]
