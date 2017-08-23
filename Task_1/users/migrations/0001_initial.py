# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-22 19:26
from __future__ import unicode_literals

import django.core.validators
import django.db.models.deletion
import django_countries.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+9999999999'.", regex='^\\+?\\d{9,15}$')])),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('image', models.ImageField(blank=True, max_length=255, null=True, upload_to='users/')),
                ('address', models.TextField(blank=True, max_length=1000)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'userprofile',
            },
        ),
    ]
