# Generated by Django 2.2.4 on 2019-08-22 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='full_name',
        ),
    ]
