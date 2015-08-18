# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('area', models.DecimalField(decimal_places=3, max_digits=100)),
                ('description', models.CharField(max_length=1024)),
                ('kind', models.CharField(max_length=255)),
                ('contact_number', models.CharField(max_length=255)),
                ('demanded_price', models.DecimalField(decimal_places=3, max_digits=100)),
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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('viewed_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('post_viewed', models.ForeignKey(related_name='post_views', to='posts.Post')),
                ('viewed_by', models.ForeignKey(related_name='views', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('message', models.CharField(max_length=512)),
                ('price', models.DecimalField(decimal_places=3, max_digits=100)),
                ('status', models.CharField(default='pending', max_length=255)),
                ('requested_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('post', models.ForeignKey(related_name='requests', to='posts.Post')),
                ('requested_by', models.ForeignKey(related_name='requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
