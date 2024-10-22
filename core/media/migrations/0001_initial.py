# Generated by Django 5.1.1 on 2024-09-29 20:03

import core.media.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('file', models.FileField(upload_to=core.media.models.PathAndRename)),
                ('file_type', models.CharField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
