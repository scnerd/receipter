# Generated by Django 4.2.3 on 2023-07-09 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("receipter", "0002_productcategory_parent_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lineitem",
            name="price",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AlterField(
            model_name="lineitem",
            name="quantity",
            field=models.DecimalField(
                blank=True, decimal_places=3, max_digits=10, null=True
            ),
        ),
        migrations.AlterField(
            model_name="lineitem",
            name="unit_price",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AlterField(
            model_name="packaging",
            name="quantity",
            field=models.DecimalField(
                blank=True, decimal_places=3, max_digits=10, null=True
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="name",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="receipt",
            name="total_paid",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
    ]
