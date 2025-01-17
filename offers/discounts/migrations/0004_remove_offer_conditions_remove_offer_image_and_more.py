# Generated by Django 5.1.1 on 2024-10-03 20:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discounts', '0003_rename_commission_percentage_marketingcoupon_commission_value_and_more'),
        ('media', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='conditions',
        ),
        migrations.RemoveField(
            model_name='offer',
            name='image',
        ),
        migrations.AddField(
            model_name='offer',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='description_en',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='name_en',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='offercondition',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='min_purchase_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True, verbose_name='Min Purchase Amount'),
        ),
        migrations.CreateModel(
            name='OfferImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('BAR', 'Bar'), ('POPUP', 'Popup'), ('CARD', 'Card'), ('PRODUCT_CARD', 'Product Card'), ('GROUP_CARD', 'Group Card'), ('CATEGORY_CARD', 'Category Card')], max_length=20)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='media.media')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discounts.offer')),
            ],
        ),
        migrations.DeleteModel(
            name='AbandonedCartOffer',
        ),
    ]
