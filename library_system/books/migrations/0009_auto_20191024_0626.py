# Generated by Django 2.2.6 on 2019-10-24 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_auto_20191024_0625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issuebook',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
