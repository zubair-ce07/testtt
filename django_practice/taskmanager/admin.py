from __future__ import absolute_import
from django.contrib import admin
from django.contrib.auth.models import Group
from django.db import models
from django.db.models import Count
from taskmanager.models import Task, CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ('assigned_by__title', 'assignee__title',)
    list_display = ('username', 'task_count',)

    def get_queryset(self, request):
        queryset = super(CustomUserAdmin, self).get_queryset(request)
        queryset_self_assigned = queryset.filter(assigned_by=models.F('assignee')).annotate(
            tasks_count=Count('assigned_by') + Count('assignee'))
        queryset = queryset.exclude(assigned_by=models.F('assignee')).annotate(tasks_count=Count('assignee'))
        return queryset_self_assigned | queryset

    def task_count(self, obj):
        return obj.tasks_count

    task_count.short_description = "No. of Tasks"


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status',)
    list_editable = ('status',)


admin.site.register(Task, TaskAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
