# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('email', models.EmailField(verbose_name='email address', unique=True, max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('gender', models.CharField(max_length=100)),
                ('dob', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('zip_code', models.CharField(max_length=50)),
                ('street', models.CharField(max_length=255)),
                ('route', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.OneToOneField(to='users.Address'),
        ),
    ]
