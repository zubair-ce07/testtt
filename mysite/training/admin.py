# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Assignment, Technology, Trainee, Trainer, UserProfile


@admin.register(Trainee)
class TraineeAdmin(admin.ModelAdmin):
    list_filter = ['trainer']


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_filter = ['user']


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_filter = ['name']
    search_fields = ['name']
    list_display = ['name']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_filter = ['technology_used', 'completion_status']
    search_fields = ['title']
    list_display = ['title', 'description']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['user']
