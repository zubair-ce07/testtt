# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-09 10:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0011_auto_20170809_0933'),
    ]

    operations = [
        migrations.AddField(
            model_name='appraisal',
            name='rating',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=5),
        ),
    ]
