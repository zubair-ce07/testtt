# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20150819_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='sold_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
