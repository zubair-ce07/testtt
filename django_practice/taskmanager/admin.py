from __future__ import absolute_import
from django.contrib import admin

# Register your models here.
from taskmanager.models import Task

admin.site.register(Task)
