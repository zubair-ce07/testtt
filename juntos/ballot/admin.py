from django.contrib import admin
from django.contrib.auth.models import User

from .models import Ballot, Choice, Vote, Tag


class ChoiceInline(admin.StackedInline):
    """
    Choices to show during adding a Ballots in Add ballot Admin panel.
    """
    model = Choice
    max_num = 3


def make_inavtive(modeladmin, request, queryset):
    """
    Make/Update selected Ballots in-active from admin panel.
    """
    queryset.update(is_active=False)


make_inavtive.short_description = "Mark selected ballots inactive."


class BallotAdmin(admin.ModelAdmin):
    """
    Ballot Admin
    """
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
    actions = [make_inavtive]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Filter users with admin status only in showing users in adding/editing Ballots.
        :param db_field: Field to show.
        :param request: Request
        :param kwargs: Key word arguments
        :return: Call super.formfield_for_foreignkey
        """
        if db_field.name == "created_by":
            kwargs["queryset"] = User.objects.filter(groups__name='Admin')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Ballot, BallotAdmin)
admin.site.register(Choice)
admin.site.register(Vote)
admin.site.register(Tag)
