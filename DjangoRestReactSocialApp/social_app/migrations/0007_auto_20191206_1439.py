# Generated by Django 2.2.7 on 2019-12-06 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_app', '0006_auto_20191205_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='post',
            name='body',
            field=models.TextField(),
        ),
    ]
