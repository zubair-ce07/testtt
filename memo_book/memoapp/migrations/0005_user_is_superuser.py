# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-13 17:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memoapp', '0004_auto_20170713_1737'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as super user or not.', verbose_name='active'),
        ),
    ]
