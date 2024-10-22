# Generated by Django 5.1.1 on 2024-09-29 20:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('branches', '0003_initial'),
        ('branches_products', '0001_initial'),
        ('branches_users', '0001_initial'),
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='primaryshelf',
            name='supervisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primary_shelves', to='branches_users.branchuser', verbose_name='Supervisor'),
        ),
        migrations.AddField(
            model_name='product',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='branches.branch', verbose_name='Branch'),
        ),
        migrations.AddField(
            model_name='product',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branches', to='products.product', verbose_name='Product'),
        ),
        migrations.AddField(
            model_name='productchangestaterequest',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='change_state_requests', to='branches_users.branchuser', verbose_name='Creator'),
        ),
        migrations.AddField(
            model_name='productchangestaterequest',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='change_state_requests', to='branches_products.product', verbose_name='Product'),
        ),
        migrations.AddField(
            model_name='productcost',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='costs', to='branches_products.product', verbose_name='Product'),
        ),
        migrations.AddField(
            model_name='productcost',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branch_products_costs', to='products.unit', verbose_name='Unit'),
        ),
        migrations.AddField(
            model_name='productprice',
            name='pricing_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='branches_products.pricinggroup', verbose_name='Pricing Group'),
        ),
        migrations.AddField(
            model_name='productprice',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='branches_products.product', verbose_name='Product'),
        ),
        migrations.AddField(
            model_name='productprice',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branch_products_prices', to='products.unit', verbose_name='Unit'),
        ),
        migrations.AddField(
            model_name='productquantity',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quantities', to='branches_products.product', verbose_name='Product'),
        ),
        migrations.AddField(
            model_name='productquantity',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.unit', verbose_name='Unit'),
        ),
        migrations.AddField(
            model_name='productsupplyaction',
            name='actor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actions_in_supply_requests', to=settings.AUTH_USER_MODEL, verbose_name='Actor'),
        ),
        migrations.AddField(
            model_name='productsupplyrequest',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_supply_requests', to='branches_users.branchuser', verbose_name='Creator'),
        ),
        migrations.AddField(
            model_name='productsupplyrequest',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supply_requests', to='branches_products.product', verbose_name='Products'),
        ),
        migrations.AddField(
            model_name='productsupplyrequest',
            name='supervisor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supervised_supply_request', to=settings.AUTH_USER_MODEL, verbose_name='Staff'),
        ),
        migrations.AddField(
            model_name='productsupplyrequest',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplied_supply_requests', to=settings.AUTH_USER_MODEL, verbose_name='Supplier'),
        ),
        migrations.AddField(
            model_name='productsupplyaction',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actions', to='branches_products.productsupplyrequest', verbose_name='Request'),
        ),
        migrations.AddField(
            model_name='producttransferrequest',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfer_requests', to='branches_users.branchuser', verbose_name='Creator'),
        ),
        migrations.AddField(
            model_name='producttransferrequest',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfer_requests', to='branches_products.product', verbose_name='Products'),
        ),
        migrations.AddField(
            model_name='shelf',
            name='products',
            field=models.ManyToManyField(related_name='shelves', to='branches_products.product', verbose_name='Products'),
        ),
        migrations.AddField(
            model_name='shelf',
            name='supervisor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shelves', to='branches_users.preparer', verbose_name='Supervisor'),
        ),
        migrations.AddField(
            model_name='producttransferrequest',
            name='from_shelf',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfer_requests', to='branches_products.shelf', verbose_name='From Shelf'),
        ),
        migrations.AddField(
            model_name='producttransferrequest',
            name='to_shelf',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receive_requests', to='branches_products.shelf', verbose_name='To Shelf'),
        ),
        migrations.AddField(
            model_name='subshelf',
            name='primary_shelf',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_shelves', to='branches_products.primaryshelf', verbose_name='Primary Shelf'),
        ),
        migrations.AddField(
            model_name='subshelf',
            name='supervisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_shelves', to='branches_users.branchuser', verbose_name='Supervisor'),
        ),
        migrations.AddField(
            model_name='shelf',
            name='sub_shelf',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shelves', to='branches_products.subshelf', verbose_name='Sub Shelf'),
        ),
        migrations.AddConstraint(
            model_name='primaryshelf',
            constraint=models.UniqueConstraint(condition=models.Q(('is_deleted', False)), fields=('index', 'branch'), name='unique_primary_shelf'),
        ),
        migrations.AddConstraint(
            model_name='product',
            constraint=models.UniqueConstraint(condition=models.Q(('is_deleted', False)), fields=('branch', 'product'), name='unique_product'),
        ),
        migrations.AddConstraint(
            model_name='productcost',
            constraint=models.UniqueConstraint(condition=models.Q(('is_deleted', False)), fields=('product', 'unit'), name='unique_product_cost'),
        ),
        migrations.AddConstraint(
            model_name='productprice',
            constraint=models.UniqueConstraint(condition=models.Q(('is_deleted', False)), fields=('product', 'unit', 'pricing_group'), name='unique_product_price'),
        ),
        migrations.AddConstraint(
            model_name='productquantity',
            constraint=models.UniqueConstraint(condition=models.Q(('is_deleted', False)), fields=('product', 'unit'), name='unique_product_quantity'),
        ),
        migrations.AddConstraint(
            model_name='subshelf',
            constraint=models.UniqueConstraint(condition=models.Q(('is_deleted', False)), fields=('index', 'primary_shelf'), name='unique_sub_shelf'),
        ),
        migrations.AddConstraint(
            model_name='shelf',
            constraint=models.UniqueConstraint(condition=models.Q(('is_deleted', False)), fields=('index', 'sub_shelf'), name='unique_shelf'),
        ),
    ]