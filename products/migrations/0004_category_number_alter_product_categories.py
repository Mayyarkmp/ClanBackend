# Generated by Django 5.1.1 on 2024-10-06 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_productprice_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='number',
            field=models.CharField(db_index=True, default=5656, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='products', to='products.category', verbose_name='Category'),
        ),
    ]
