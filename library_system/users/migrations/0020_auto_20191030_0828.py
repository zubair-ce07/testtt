# Generated by Django 2.2.6 on 2019-10-30 08:28

from __future__ import unicode_literals

from django.db import migrations

from users.constants import LIBRARIAN_GROUP_NAME




def create_librarian_group(apps, _schema_editor):
    """
    Call When migration run

    :param apps:
    :param _schema_editor:
    :return:
    """
    _Group = apps.get_model('auth', 'Group')
    _Group.objects.create(name=LIBRARIAN_GROUP_NAME)


def reverse_amount_form_read_only_group(apps, _schema_editor):
    """
    Call when migration rollback

    :param apps:
    :param _schema_editor:
    :return:
    """
    _Group = apps.get_model('auth', 'Group')
    _Group.objects.filter(name=LIBRARIAN_GROUP_NAME).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_remove_userprofile_book_count'),
    ]

    operations = [
        migrations.RunPython(create_librarian_group, reverse_amount_form_read_only_group)
    ]
