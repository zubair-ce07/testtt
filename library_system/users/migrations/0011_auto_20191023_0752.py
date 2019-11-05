# Generated by Django 2.2.6 on 2019-10-23 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_auto_20191022_1011'),
        ('users', '0010_auto_20191023_0734'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='books',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='books',
            field=models.ForeignKey(max_length=3, null=True, on_delete=django.db.models.deletion.CASCADE, to='books.Book'),
        ),
    ]
