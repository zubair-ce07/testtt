# Generated by Django 2.1.5 on 2019-02-04 12:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20190204_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='completion_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 24, 12, 13, 27, 54675)),
        ),
    ]
