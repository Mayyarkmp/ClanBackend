# Generated by Django 5.1.1 on 2024-09-29 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BrowsingKey',
            fields=[
                ('key', models.CharField(max_length=24, primary_key=True, serialize=False)),
                ('delivery_type', models.CharField(choices=[('FAST', 'Fast'), ('SCHEDULED', 'Scheduled')], default='FAST', max_length=10)),
            ],
        ),
    ]