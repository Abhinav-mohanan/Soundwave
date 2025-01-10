# Generated by Django 5.1.3 on 2024-12-23 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_order_items_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_items',
            name='status',
            field=models.CharField(choices=[('Pending', 'Order Pending'), ('Confirmed', ' Order Confirmed'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Order Pending', max_length=20),
        ),
    ]
