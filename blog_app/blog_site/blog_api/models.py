# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=100)
    categories = models.CharField(max_length=1000)
    content = models.CharField(max_length=2000)
