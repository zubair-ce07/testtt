# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Trainee, Trainer, Technology, Assignment

admin.site.register(Trainee)
admin.site.register(Trainer)
admin.site.register(Technology)
admin.site.register(Assignment)
