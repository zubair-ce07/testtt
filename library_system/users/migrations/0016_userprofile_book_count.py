# Generated by Django 2.2.6 on 2019-10-24 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_remove_userprofile_book_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='book_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
