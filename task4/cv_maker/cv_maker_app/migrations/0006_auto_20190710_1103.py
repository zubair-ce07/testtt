# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-10 11:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cv_maker_app', '0005_basicinformation_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicinformation',
            name='image',
            field=models.ImageField(upload_to=b''),
        ),
    ]
