from django.contrib import admin
from django.contrib.auth.models import User

from .models import Ballot, Choice, Vote, Tag


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class BallotAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title']}),
        ('Period:', {'fields': ['active_period', 'is_active']}),
        ('Tags', {'fields': ['tags']}),
        ('Added by', {'fields': ['created_by']})
    ]
    inlines = [ChoiceInline]
    list_display = ('title', 'is_active', 'created_by', 'ending_date')
    list_filter = ['created_at', 'is_active', 'created_by']
    search_fields = ['title']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "created_by":
            kwargs["queryset"] = User.objects.filter(groups__name='Admin')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Ballot, BallotAdmin)
admin.site.register(Choice)
admin.site.register(Vote)
admin.site.register(Tag)
