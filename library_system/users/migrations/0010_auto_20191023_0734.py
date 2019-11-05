# Generated by Django 2.2.6 on 2019-10-23 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_auto_20191022_1011'),
        ('users', '0009_auto_20191023_0650'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='books_issued',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='books',
            field=models.ManyToManyField(blank=True, max_length=3, to='books.Book'),
        ),
    ]
