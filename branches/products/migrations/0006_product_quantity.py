# Generated by Django 5.1.1 on 2024-10-12 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branches_products', '0005_remove_productcost_product_remove_productcost_unit_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(default=0, verbose_name='Quantity'),
        ),
    ]
