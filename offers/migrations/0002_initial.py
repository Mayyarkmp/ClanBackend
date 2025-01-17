# Generated by Django 5.1.1 on 2024-09-29 20:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('branches', '0003_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('customers', '0002_initial'),
        ('discounts', '0002_initial'),
        ('offers', '0001_initial'),
        ('products', '0001_initial'),
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotionanalytics',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customers.customer'),
        ),
        migrations.AddField(
            model_name='promotionanalytics',
            name='offer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='analytics', to='discounts.offer'),
        ),
        migrations.AddField(
            model_name='promotionanalytics',
            name='zone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='settings.geographicalzone'),
        ),
        migrations.AddField(
            model_name='promotionbranchlimit',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='promotion_limits', to='branches.branch'),
        ),
        migrations.AddField(
            model_name='promotioncondition',
            name='applicable_branches',
            field=models.ManyToManyField(blank=True, to='branches.branch', verbose_name='Applicable Branches'),
        ),
        migrations.AddField(
            model_name='promotioncondition',
            name='applicable_cities',
            field=models.ManyToManyField(blank=True, to='settings.city', verbose_name='Applicable Cities'),
        ),
        migrations.AddField(
            model_name='promotioncondition',
            name='applicable_countries',
            field=models.ManyToManyField(blank=True, to='settings.country', verbose_name='Applicable Countries'),
        ),
        migrations.AddField(
            model_name='promotioncondition',
            name='applicable_regions',
            field=models.ManyToManyField(blank=True, to='settings.region', verbose_name='Applicable Regions'),
        ),
        migrations.AddField(
            model_name='promotioncondition',
            name='applicable_sub_regions',
            field=models.ManyToManyField(blank=True, to='settings.subregion', verbose_name='Applicable SubRegions'),
        ),
        migrations.AddField(
            model_name='promotioncondition',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='promotioncondition',
            name='excluded_brands',
            field=models.ManyToManyField(blank=True, related_name='excluded_from_promotions', to='products.brand', verbose_name='Excluded Brands'),
        ),
        migrations.AddField(
            model_name='promotioncondition',
            name='excluded_categories',
            field=models.ManyToManyField(blank=True, related_name='excluded_from_promotions', to='products.category', verbose_name='Excluded Categories'),
        ),
        migrations.AddField(
            model_name='promotioncondition',
            name='excluded_groups',
            field=models.ManyToManyField(blank=True, related_name='excluded_from_promotions', to='products.group', verbose_name='Excluded Groups'),
        ),
        migrations.AddField(
            model_name='promotioncondition',
            name='excluded_payment_services',
            field=models.ManyToManyField(blank=True, related_name='excluded_from_promotions', to='settings.paymentservice', verbose_name='Excluded Payment Services'),
        ),
        migrations.AddField(
            model_name='promotioncondition',
            name='excluded_products',
            field=models.ManyToManyField(blank=True, related_name='excluded_from_promotions', to='products.product', verbose_name='Excluded Products'),
        ),
        migrations.AddField(
            model_name='promotioncondition',
            name='excluded_suppliers',
            field=models.ManyToManyField(blank=True, related_name='excluded_from_promotions', to='products.supplier', verbose_name='Excluded Suppliers'),
        ),
        migrations.AddField(
            model_name='promotioncondition',
            name='included_brands',
            field=models.ManyToManyField(blank=True, related_name='included_in_promotions', to='products.brand', verbose_name='Included Brands'),
        ),
        migrations.AddField(
            model_name='promotioncondition',
            name='included_categories',
            field=models.ManyToManyField(blank=True, related_name='included_in_promotions', to='products.category', verbose_name='Included Categories'),
        ),
        migrations.AddField(
            model_name='promotioncondition',
            name='included_groups',
            field=models.ManyToManyField(blank=True, related_name='included_in_promotions', to='products.group', verbose_name='Included Groups'),
        ),
        migrations.AddField(
            model_name='promotioncondition',
            name='included_payment_services',
            field=models.ManyToManyField(blank=True, related_name='included_in_promotions', to='settings.paymentservice', verbose_name='Included Payment Services'),
        ),
        migrations.AddField(
            model_name='promotioncondition',
            name='included_products',
            field=models.ManyToManyField(blank=True, related_name='included_in_promotions', to='products.product', verbose_name='Included Products'),
        ),
        migrations.AddField(
            model_name='promotioncondition',
            name='included_suppliers',
            field=models.ManyToManyField(blank=True, related_name='included_in_promotions', to='products.supplier', verbose_name='Included Suppliers'),
        ),
        migrations.AddField(
            model_name='promotionbranchlimit',
            name='promotion_condition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branch_limits', to='offers.promotioncondition'),
        ),
        migrations.AddField(
            model_name='promotionregionlimit',
            name='promotion_condition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='region_limits', to='offers.promotioncondition'),
        ),
        migrations.AddField(
            model_name='promotionregionlimit',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='promotion_limits', to='settings.region'),
        ),
        migrations.AddField(
            model_name='promotiontimeslot',
            name='promotion_condition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_slots', to='offers.promotioncondition'),
        ),
        migrations.AddField(
            model_name='promotionusage',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='branches.branch'),
        ),
        migrations.AddField(
            model_name='promotionusage',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customers.customer'),
        ),
        migrations.AddField(
            model_name='promotionusage',
            name='promotion_condition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usages', to='offers.promotioncondition'),
        ),
        migrations.AddField(
            model_name='promotionusage',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='settings.region'),
        ),
        migrations.AlterUniqueTogether(
            name='promotionbranchlimit',
            unique_together={('promotion_condition', 'branch')},
        ),
        migrations.AlterUniqueTogether(
            name='promotionregionlimit',
            unique_together={('promotion_condition', 'region')},
        ),
    ]
