# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='picture',
            name='post',
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='post',
            name='kind',
            field=models.CharField(max_length=255, choices=[('house', 'House'), ('plot', 'Plot'), ('commercial_plot', 'Commercial Plot'), ('commercial_building', 'Commercial Building'), ('flat', 'Flat'), ('shop', 'Shop'), ('farm_house', 'Farm House')]),
        ),
        migrations.AlterField(
            model_name='post',
            name='sold_on',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.CharField(default='pending', max_length=255, choices=[('pending', 'pending'), ('rejected', 'rejected'), ('accepted', 'accepted')]),
        ),
        migrations.DeleteModel(
            name='Picture',
        ),
    ]
