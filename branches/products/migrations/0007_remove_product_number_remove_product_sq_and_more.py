# Generated by Django 5.1.1 on 2024-10-14 00:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branches_products', '0006_product_quantity'),
        ('products', '0009_alter_product_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='number',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sq',
        ),
        migrations.AddField(
            model_name='product',
            name='serial_number',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Serial Number'),
        ),
        migrations.AddField(
            model_name='product',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='branches_products', to='products.supplier', verbose_name='Supplier'),
        ),
    ]
