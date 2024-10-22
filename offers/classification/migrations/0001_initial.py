# Generated by Django 5.1.1 on 2024-09-29 20:03

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('media', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('per', models.CharField(choices=[('GROUP', 'Group'), ('CATEGORY', 'Category'), ('SUPPLIER', 'Supplier'), ('PRODUCT', 'Product'), ('MIXIN', 'Mixin')], max_length=10)),
                ('is_draft', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=False)),
                ('images', models.ManyToManyField(blank=True, related_name='packs', to='media.media')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='offers_classification.pack')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PackCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pack_packs', to='products.category')),
                ('pack', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pack_categories', to='offers_classification.pack')),
            ],
            options={
                'unique_together': {('pack', 'category')},
            },
        ),
        migrations.AddField(
            model_name='pack',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='packs', through='offers_classification.PackCategory', to='products.category', verbose_name='Categories'),
        ),
        migrations.CreateModel(
            name='PackGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pack_packs', to='products.group')),
                ('pack', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pack_groups', to='offers_classification.pack')),
            ],
            options={
                'unique_together': {('pack', 'group')},
            },
        ),
        migrations.AddField(
            model_name='pack',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='packs', through='offers_classification.PackGroup', to='products.group', verbose_name='Groups'),
        ),
        migrations.CreateModel(
            name='PackProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('pack', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pack_products', to='offers_classification.pack')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pack_packs', to='products.product')),
            ],
            options={
                'unique_together': {('pack', 'product')},
            },
        ),
        migrations.AddField(
            model_name='pack',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='packs', through='offers_classification.PackProduct', to='products.product', verbose_name='Products'),
        ),
        migrations.CreateModel(
            name='PackSupplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('pack', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pack_suppliers', to='offers_classification.pack')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pack_packs', to='products.supplier')),
            ],
            options={
                'unique_together': {('pack', 'supplier')},
            },
        ),
        migrations.AddField(
            model_name='pack',
            name='suppliers',
            field=models.ManyToManyField(blank=True, related_name='packs', through='offers_classification.PackSupplier', to='products.supplier', verbose_name='Suppliers'),
        ),
    ]
