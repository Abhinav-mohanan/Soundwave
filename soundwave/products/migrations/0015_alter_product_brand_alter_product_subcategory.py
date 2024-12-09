# Generated by Django 5.1.3 on 2024-12-04 18:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_category_image_product_subcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brand_product', to='products.brand'),
        ),
        migrations.AlterField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategory_product', to='products.subcategory'),
        ),
    ]
