# Generated by Django 5.1.1 on 2024-10-07 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='data',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
