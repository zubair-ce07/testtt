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
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(nps__gte=0, nps__lte=3)

class SatisfactionlevelListFilter(SimpleListFilter):
    title = _('Satisfaction Level')
    parameter_name = 'satisfaction_level'

    def lookups(self, request, model_admin):
        return (
            ('0', _('0-3')),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(satisfaction_level__gte=0, satisfaction_level__lte=3)


class FeedbacksAdmin(admin.ModelAdmin):
    search_fields = ('name', 'comment')
    list_filter = ('department', 'store', NpsListFilter, SatisfactionlevelListFilter)
    list_display = [field.name for field in Feedbacks._meta.fields]


admin.site.register(Feedbacks, FeedbacksAdmin)
admin.site.register(Department)
admin.site.register(Store)
