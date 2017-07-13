from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _

from .models import Feedbacks, Department, Store


class NpsListFilter(SimpleListFilter):
    title = _('NPS')
    parameter_name = 'nps'

    def lookups(self, request, model_admin):
        return (
            ('0', _('0-3')),
            ('4', _('4-7')),
            ('8', _('8-10')),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(nps__range=(0, 3))
        if self.value() == '4':
            return queryset.filter(nps__range=(4, 7))
        if self.value() == '8':
            return queryset.filter(nps__range=(8, 10))


class SatisfactionlevelListFilter(SimpleListFilter):
    title = _('Satisfaction Level')
    parameter_name = 'satisfaction_level'

    def lookups(self, request, model_admin):
        return (
            ('0', _('0-3')),
            ('4', _('4-7')),
            ('8', _('8-10')),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(satisfaction_level__range=(0, 3))
        if self.value() == '4':
            return queryset.filter(satisfaction_level__range=(4, 7))
        if self.value() == '8':
            return queryset.filter(satisfaction_level__range=(8, 10))


class FeedbacksAdmin(admin.ModelAdmin):
    search_fields = ('name', 'comment')
    list_filter = ('department', 'store', NpsListFilter, SatisfactionlevelListFilter)
    list_display = ['name', 'cell_phone', 'email', 'age', 'gender',
                    'comment', 'nps', 'satisfaction_level', 'department',
                    'store', 'created_at']


admin.site.register(Feedbacks, FeedbacksAdmin)
admin.site.register(Department)
admin.site.register(Store)
