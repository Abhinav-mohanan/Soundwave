# Generated by Django 5.1.3 on 2024-12-10 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_wishlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wishlist',
            old_name='product',
            new_name='variant',
        ),
    ]
