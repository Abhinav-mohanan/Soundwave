# Generated by Django 5.1.3 on 2024-12-20 04:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0003_alter_brand_offer_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='brand_offer',
            old_name='offer_price',
            new_name='offer_percentage',
        ),
        migrations.RenameField(
            model_name='product_offer',
            old_name='offer_price',
            new_name='offer_percentage',
        ),
    ]
