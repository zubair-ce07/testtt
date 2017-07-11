from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _

from .models import Feedbacks, Department, Store


class NpsListFilter(SimpleListFilter):
    title = _('NPS')
    parameter_name = 'nps'

    def lookups(self, request, model_admin):
        return (
            ('0', _('0')),
            ('1', _('1')),
            ('2', _('2')),
            ('3', _('3')),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(nps=0)
        if self.value() == '1':
            return queryset.filter(nps=1)
        if self.value() == '2':
            return queryset.filter(nps=2)
        if self.value() == '3':
            return queryset.filter(nps=3)


class SatisfactionlevelListFilter(SimpleListFilter):
    title = _('Satisfaction Level')
    parameter_name = 'satisfaction_level'

    def lookups(self, request, model_admin):
        return (
            ('0', _('0')),
            ('1', _('1')),
            ('2', _('2')),
            ('3', _('3')),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(satisfaction_level=0)
        if self.value() == '1':
            return queryset.filter(satisfaction_level=1)
        if self.value() == '2':
            return queryset.filter(satisfaction_level=2)
        if self.value() == '3':
            return queryset.filter(satisfaction_level=3)


class FeedbacksAdmin(admin.ModelAdmin):
    search_fields = ('name', 'comment')
    list_filter = ('department', 'store', NpsListFilter, SatisfactionlevelListFilter)
    list_display = [field.name for field in Feedbacks._meta.fields]


admin.site.register(Feedbacks, FeedbacksAdmin)
admin.site.register(Department)
admin.site.register(Store)
