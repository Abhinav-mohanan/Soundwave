# Generated by Django 5.1.3 on 2024-12-02 06:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('address_title', models.CharField(default='Home', max_length=50)),
                ('state', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('pin', models.CharField(max_length=6)),
                ('address_line1', models.CharField(max_length=100)),
                ('address_line2', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
