# Generated by Django 5.1.1 on 2024-09-30 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='created',
        ),
    ]
