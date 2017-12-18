# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-17 05:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20170714_0705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='gender',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='product',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to=settings.AUTH_USER_MODEL),
        ),
    ]
