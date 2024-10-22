# Generated by Django 5.1.1 on 2024-10-08 00:16

import django.db.models.deletion
import orders.models
import uuid
from django.db import migrations, models


def populate_order_numbers(apps, schema_editor):
    Order = apps.get_model("orders", "Order")
    db_alias = schema_editor.connection.alias
    with schema_editor.connection.cursor() as cursor:
        for order in Order.objects.using(db_alias).filter(number__isnull=True):
            cursor.execute("SELECT nextval('orders_order_number_seq')")
            result = cursor.fetchone()
            order_number = result[0]
            order.number = order_number
            order.save()


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0017_rename_discount_id_cartitem_offer_id_and_more"),
        ("products", "0005_alter_barcode_options_alter_brand_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderBlock",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "uid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="cartpromotion",
            name="uid",
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
        migrations.AddField(
            model_name="order",
            name="number",
            field=models.PositiveBigIntegerField(null=True),
        ),
        migrations.RunSQL(
            """
            CREATE SEQUENCE orders_order_number_seq OWNED BY orders_order.number;
            """,
            reverse_sql="DROP SEQUENCE orders_order_number_seq;",
        ),
        migrations.RunPython(populate_order_numbers),
        migrations.AlterField(
            model_name="order",
            name="number",
            field=models.PositiveBigIntegerField(
                unique=True, null=False, editable=False
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="number",
            field=models.PositiveBigIntegerField(
                default=orders.models.get_order_number,
                unique=True,
                editable=False,
            ),
        ),
        migrations.AlterField(
            model_name="cart",
            name="status",
            field=models.CharField(
                choices=[
                    ("OPEN", "Open"),
                    ("CLOSED", "Closed"),
                    ("ORDERED", "Ordered"),
                    ("CANCELED", "Canceled"),
                    ("ABANDONED", "Abandoned"),
                ],
                default="OPEN",
                max_length=50,
            ),
        ),
        migrations.CreateModel(
            name="OrderBlockItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "uid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("quantity", models.PositiveIntegerField(default=1)),
                (
                    "block",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="orders.orderblock",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="block_items",
                        to="products.product",
                    ),
                ),
                (
                    "unit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="block_items",
                        to="products.unit",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]