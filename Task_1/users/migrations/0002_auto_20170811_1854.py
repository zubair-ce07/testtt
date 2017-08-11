# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-11 13:54
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+9999999999'.", regex='^\\+?\\d{9,15}$')]),
        ),
    ]
