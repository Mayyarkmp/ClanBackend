# Generated by Django 5.1.1 on 2024-10-07 12:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('orders', '0016_rename_discount_value_cartitem_discount_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='discount_id',
            new_name='offer_id',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='discount_currency',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='discount_type',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='offer_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cart_items_offers', to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='offer_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]