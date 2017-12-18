# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 07:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myfacebook', '0002_auto_20171027_0734'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userfollowers',
            options={'verbose_name_plural': 'UserFollowers'},
        ),
        migrations.AlterField(
            model_name='userstatus',
            name='status_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to='myfacebook.UserProfile'),
        ),
    ]
