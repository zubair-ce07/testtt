# Generated by Django 2.1.1 on 2018-09-27 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0005_auto_20180926_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='last_edit',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='issue',
            name='last_edit',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
