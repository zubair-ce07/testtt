# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class DateTime(models.Model):
    date = models.DateTimeField()

    def __str__(self):
        return str(self.date)