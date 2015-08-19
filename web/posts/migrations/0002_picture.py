# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('image', models.FileField(upload_to='images/')),
                ('is_expired', models.BooleanField(default=False)),
                ('post', models.ForeignKey(to='posts.Post', related_name='pictures')),
            ],
        ),
    ]
