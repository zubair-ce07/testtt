# Generated by Django 2.2.4 on 2019-09-04 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20190904_0704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='reservation',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shop.TimeSlot'),
        ),
    ]
