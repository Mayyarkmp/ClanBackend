# Generated by Django 5.1.1 on 2024-09-29 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='name',
            field=models.CharField(db_index=True, default=1, max_length=100, verbose_name='Name'),
            preserve_default=False,
        ),
    ]
