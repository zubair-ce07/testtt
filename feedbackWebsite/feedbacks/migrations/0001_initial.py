# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-07 06:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedbacks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.CharField(blank=True, max_length=254)),
                ('name', models.CharField(blank=True, max_length=254)),
                ('cell_phone', models.CharField(blank=True, max_length=254)),
                ('email', models.CharField(blank=True, max_length=254)),
                ('age', models.CharField(blank=True, max_length=254)),
                ('gender', models.CharField(blank=True, max_length=254)),
                ('store', models.CharField(blank=True, max_length=254)),
                ('department', models.CharField(blank=True, max_length=254)),
                ('comment', models.CharField(blank=True, max_length=1000)),
                ('nps', models.CharField(blank=True, max_length=254)),
                ('satisfaction_level', models.CharField(blank=True, max_length=254)),
            ],
        ),
    ]
