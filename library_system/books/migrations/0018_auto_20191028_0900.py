# Generated by Django 2.2.6 on 2019-10-28 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0017_requestbook'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestbook',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
