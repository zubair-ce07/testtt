# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 07:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myfacebook', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfollowers',
            name='followee',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='followee', to='myfacebook.UserProfile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userfollowers',
            name='follower',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='myfacebook.UserProfile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userstatus',
            name='status_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myfacebook.UserProfile'),
        ),
        migrations.RemoveField(
            model_name='userfollowers',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='userfollowers',
            unique_together=set([('followee', 'follower')]),
        ),
    ]
