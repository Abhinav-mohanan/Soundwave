# Generated by Django 5.1.3 on 2024-11-23 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_remove_products_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='is_listd',
            field=models.BooleanField(default=True),
        ),
    ]
