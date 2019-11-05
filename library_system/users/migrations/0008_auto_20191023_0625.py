# Generated by Django 2.2.6 on 2019-10-23 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_auto_20191022_1011'),
        ('users', '0007_auto_20191023_0614'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='books_issued',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='books.Book'),
        ),
        migrations.DeleteModel(
            name='BooksIssued',
        ),
    ]
