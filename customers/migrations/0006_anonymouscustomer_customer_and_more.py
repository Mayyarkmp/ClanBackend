# Generated by Django 5.1.1 on 2024-10-06 13:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_browsingkey_anonymous'),
        ('sessions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='anonymouscustomer',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customers.customer'),
        ),
        migrations.AddField(
            model_name='anonymouscustomer',
            name='sessions',
            field=models.ManyToManyField(blank=True, to='sessions.session'),
        ),
    ]