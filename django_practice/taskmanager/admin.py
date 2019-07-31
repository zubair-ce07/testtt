from __future__ import absolute_import
from django.contrib import admin
from taskmanager.models import Task, CustomUser

admin.site.register(Task)
admin.site.register(CustomUser)
