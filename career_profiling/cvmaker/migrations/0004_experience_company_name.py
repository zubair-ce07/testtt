# Generated by Django 2.2.7 on 2019-11-26 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cvmaker', '0003_auto_20191126_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='experience',
            name='company_name',
            field=models.CharField(default='', max_length=500),
        ),
    ]
