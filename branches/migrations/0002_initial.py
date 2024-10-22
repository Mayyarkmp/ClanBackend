# Generated by Django 5.1.1 on 2024-09-29 20:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('branches', '0001_initial'),
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='settings.city'),
        ),
        migrations.AddField(
            model_name='branch',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='settings.country'),
        ),
    ]
