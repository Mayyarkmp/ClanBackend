# Generated by Django 5.1.1 on 2024-09-30 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'base_manager_name': 'objects'},
        ),
    ]
