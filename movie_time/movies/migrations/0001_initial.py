# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-31 07:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('month', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('year', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aspect_ratio', models.FloatField(blank=True, null=True)),
                ('file_path', models.CharField(max_length=40)),
                ('height', models.IntegerField(blank=True, null=True)),
                ('width', models.IntegerField(blank=True, null=True)),
                ('iso_639_1', models.CharField(blank=True, max_length=2, null=True)),
                ('vote_average', models.FloatField(blank=True, null=True)),
                ('vote_count', models.IntegerField(blank=True, null=True)),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Backdrop'), (2, 'Poster'), (3, 'Profile')])),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=100)),
                ('credit_id', models.CharField(max_length=40, unique=True)),
                ('job', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adult', models.BooleanField()),
                ('budget', models.IntegerField()),
                ('homepage', models.TextField(blank=True, null=True)),
                ('tmdb_id', models.IntegerField(unique=True)),
                ('original_language', models.CharField(max_length=30)),
                ('original_title', models.CharField(max_length=200)),
                ('overview', models.TextField(blank=True, null=True)),
                ('popularity', models.FloatField()),
                ('revenue', models.IntegerField()),
                ('runtime', models.IntegerField()),
                ('status', models.CharField(blank=True, max_length=30, null=True)),
                ('tag_line', models.CharField(blank=True, max_length=300, null=True)),
                ('title', models.CharField(max_length=200)),
                ('vote_average', models.FloatField()),
                ('vote_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adult', models.NullBooleanField()),
                ('biography', models.TextField(blank=True, null=True)),
                ('gender', models.PositiveSmallIntegerField(choices=[(0, '---'), (1, 'Female'), (2, 'Male')])),
                ('homepage', models.CharField(blank=True, max_length=200, null=True)),
                ('tmdb_id', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=100)),
                ('place_of_birth', models.CharField(blank=True, max_length=200, null=True)),
                ('popularity', models.FloatField(blank=True, null=True)),
                ('birthday', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='birthday', to='movies.Date')),
                ('deathday', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deathday', to='movies.Date')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character', models.TextField()),
                ('credit_id', models.CharField(max_length=40, unique=True)),
                ('order', models.PositiveSmallIntegerField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Movie')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Person')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tmdb_id', models.CharField(max_length=40, unique=True)),
                ('iso_639_1', models.CharField(max_length=2)),
                ('iso_3166_1', models.CharField(max_length=2)),
                ('key', models.CharField(max_length=40)),
                ('name', models.CharField(max_length=200)),
                ('site', models.CharField(max_length=40)),
                ('size', models.IntegerField()),
                ('type', models.CharField(choices=[('Trailer', 'Trailer'), ('Teaser', 'Teaser'), ('Clip', 'Clip'), ('Featurette', 'Featurette')], max_length=10)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Movie')),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='cast',
            field=models.ManyToManyField(related_name='roles', through='movies.Role', to='movies.Person'),
        ),
        migrations.AddField(
            model_name='movie',
            name='crew',
            field=models.ManyToManyField(related_name='jobs', through='movies.Job', to='movies.Person'),
        ),
        migrations.AddField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(related_name='movies', to='movies.Genre'),
        ),
        migrations.AddField(
            model_name='movie',
            name='release_date',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.Date'),
        ),
        migrations.AddField(
            model_name='job',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Movie'),
        ),
        migrations.AddField(
            model_name='job',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Person'),
        ),
    ]
