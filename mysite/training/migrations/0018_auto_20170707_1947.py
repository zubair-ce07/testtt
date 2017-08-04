# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-07 14:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0017_auto_20170707_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainee',
            name='assignments',
            field=models.ManyToManyField(default=None, to='training.Assignment'),
        ),
        migrations.AlterField(
            model_name='trainee',
            name='trainer',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='trainees', to='training.Trainer'),
        ),
    ]
