# Generated by Django 2.2.3 on 2019-07-12 06:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0006_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='created_on',
        ),
    ]
