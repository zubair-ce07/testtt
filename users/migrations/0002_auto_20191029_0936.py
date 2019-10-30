# Generated by Django 2.2.6 on 2019-10-29 09:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(default='', max_length=100, validators=[django.core.validators.RegexValidator(message='Mobile Number.', regex='^[\\d]{4}-[\\d]{7}$')]),
        ),
    ]
