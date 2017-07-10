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
    filter_horizontal = ('technology_used',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['user']
    list_display = ['name', 'user']
    fields = ['name', 'user']
    raw_id_fields = ('user',)

    # A template for a very customized change view:
    change_form_template = 'training/admin/change_form.html'

    def get_osm_info(self):
        pass

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['osm_data'] = self.get_osm_info()
        return super(UserProfileAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context, )
