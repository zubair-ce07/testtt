# Generated by Django 2.2.4 on 2019-09-04 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Fila', '0005_auto_20190904_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skus',
            name='Price',
            field=models.CharField(max_length=50),
        ),
    ]
