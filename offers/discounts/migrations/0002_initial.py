# Generated by Django 5.1.1 on 2024-09-29 20:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('discounts', '0001_initial'),
        ('media', '0001_initial'),
        ('offers', '0001_initial'),
        ('offers_classification', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='conditions',
            field=models.ManyToManyField(related_name='offers', to='offers.promotioncondition'),
        ),
        migrations.AddField(
            model_name='offer',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='media.media'),
        ),
        migrations.AddField(
            model_name='offercondition',
            name='brands_buy',
            field=models.ManyToManyField(blank=True, related_name='brand_buy_conditions', to='products.brand'),
        ),
        migrations.AddField(
            model_name='offercondition',
            name='brands_get',
            field=models.ManyToManyField(blank=True, related_name='brand_get_conditions', to='products.brand'),
        ),
        migrations.AddField(
            model_name='offercondition',
            name='categories_buy',
            field=models.ManyToManyField(blank=True, related_name='category_buy_conditions', to='products.category'),
        ),
        migrations.AddField(
            model_name='offercondition',
            name='categories_get',
            field=models.ManyToManyField(blank=True, related_name='category_get_conditions', to='products.category'),
        ),
        migrations.AddField(
            model_name='offercondition',
            name='groups_buy',
            field=models.ManyToManyField(blank=True, related_name='group_buy_conditions', to='products.group'),
        ),
        migrations.AddField(
            model_name='offercondition',
            name='groups_get',
            field=models.ManyToManyField(blank=True, related_name='group_get_conditions', to='products.group'),
        ),
        migrations.AddField(
            model_name='offercondition',
            name='offer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer_conditions', to='discounts.offer'),
        ),
        migrations.AddField(
            model_name='offercondition',
            name='packs_buy',
            field=models.ManyToManyField(blank=True, related_name='pack_buy_conditions', to='offers_classification.pack'),
        ),
        migrations.AddField(
            model_name='offercondition',
            name='packs_get',
            field=models.ManyToManyField(blank=True, related_name='pack_get_conditions', to='offers_classification.pack'),
        ),
        migrations.AddField(
            model_name='offercondition',
            name='products_buy',
            field=models.ManyToManyField(blank=True, related_name='buy_conditions', to='products.product'),
        ),
        migrations.AddField(
            model_name='offercondition',
            name='products_get',
            field=models.ManyToManyField(blank=True, related_name='get_conditions', to='products.product'),
        ),
    ]
