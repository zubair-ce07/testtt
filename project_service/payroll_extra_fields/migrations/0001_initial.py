# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-01-08 12:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payslip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('odoo_payslip_id', models.IntegerField(unique=True)),
                ('description', models.TextField()),
                ('is_reviewed', models.BooleanField(default=False)),
            ],
        ),
    ]
