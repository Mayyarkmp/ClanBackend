# Generated by Django 5.1.1 on 2024-09-29 20:03

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('media', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('type', models.CharField(choices=[('MOBILE', 'Mobile'), ('WEB', 'Web')], max_length=50)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('title_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='English Title')),
                ('slug', models.SlugField(max_length=255)),
                ('is_draft', models.BooleanField(default=True)),
                ('is_default', models.BooleanField(default=False)),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('type', 'slug'), name='unique_type_slug')],
            },
        ),
        migrations.CreateModel(
            name='DeliveryTypeContents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('type', models.CharField(choices=[('FAST', 'Fast'), ('SCHEDULED', 'Scheduled')], default='FAST', max_length=10)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('short_description', models.TextField(blank=True, verbose_name='Short Description')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('name_en', models.CharField(blank=True, max_length=50, null=True, verbose_name='English Name')),
                ('short_description_en', models.TextField(blank=True, verbose_name='English Short Description')),
                ('description_en', models.TextField(blank=True, verbose_name='English Description')),
                ('is_draft', models.BooleanField(default=True)),
                ('is_default', models.BooleanField(default=False)),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='media.media')),
            ],
            options={
                'verbose_name': 'Delivery Type Content',
                'verbose_name_plural': 'Delivery Type Contents',
                'constraints': [models.UniqueConstraint(condition=models.Q(('is_default', True), ('is_deleted', False), ('is_draft', False)), fields=('type',), name='unique_delivery_type_active_content')],
            },
        ),
    ]