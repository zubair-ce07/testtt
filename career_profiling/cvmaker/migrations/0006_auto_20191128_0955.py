# Generated by Django 2.2.7 on 2019-11-28 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cvmaker', '0005_auto_20191128_0954'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookmarkcv',
            old_name='profile_bookmarked',
            new_name='profile_bookmarked_id',
        ),
    ]
