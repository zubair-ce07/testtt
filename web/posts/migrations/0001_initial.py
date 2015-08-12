# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('url', models.CharField(max_length=1024)),
                ('is_expired', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('area', models.DecimalField(max_digits=100, decimal_places=3)),
                ('description', models.CharField(max_length=1024)),
                ('kind', models.CharField(max_length=255)),
                ('contact_number', models.CharField(max_length=255)),
                ('demanded_price', models.DecimalField(max_digits=100, decimal_places=3)),
                ('is_sold', models.BooleanField(default=False)),
                ('sold_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('posted_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('expired_on', models.DateTimeField()),
                ('is_expired', models.BooleanField(default=False)),
                ('location', models.OneToOneField(to='users.Address')),
                ('posted_by', models.ForeignKey(related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostView',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('viewed_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('post_viewed', models.ForeignKey(related_name='post_views', to='posts.Post')),
                ('viewed_by', models.ForeignKey(related_name='views', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('message', models.CharField(max_length=512)),
                ('price', models.DecimalField(max_digits=100, decimal_places=3)),
                ('status', models.CharField(max_length=255, default='pending')),
                ('requested_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('post', models.ForeignKey(related_name='requests', to='posts.Post')),
                ('requested_by', models.ForeignKey(related_name='requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='picture',
            name='post',
            field=models.ForeignKey(related_name='pictures', to='posts.Post'),
        ),
    ]
