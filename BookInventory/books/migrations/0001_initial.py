# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-02 06:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('address', models.CharField(max_length=256)),
                ('contact', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=254)),
                ('city', models.CharField(max_length=64)),
                ('country', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512)),
                ('genre', models.CharField(choices=[(1, 'Novel'), (2, 'Thriller'), (3, 'Drama'), (4, 'Biograghy'), (5, 'Text Book'), (6, 'Science'), (7, 'Not Specified')], default='Not Specified', max_length=64)),
                ('pub_date', models.DateField(default=b'02.08.2017')),
                ('authors', models.ManyToManyField(to='books.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('address', models.CharField(max_length=256)),
                ('contact', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=254)),
                ('city', models.CharField(max_length=64)),
                ('country', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Publisher'),
        ),
    ]
