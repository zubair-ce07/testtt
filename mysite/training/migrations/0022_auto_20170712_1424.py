# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-12 09:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0021_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datetime',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
