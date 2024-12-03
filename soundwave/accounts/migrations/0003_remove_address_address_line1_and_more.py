# Generated by Django 5.1.3 on 2024-12-02 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_address_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='address_line1',
        ),
        migrations.RemoveField(
            model_name='address',
            name='address_line2',
        ),
        migrations.AddField(
            model_name='address',
            name='detail_address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='landmark',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
