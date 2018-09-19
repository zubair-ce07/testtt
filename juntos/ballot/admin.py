from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import format_html

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
    date_hierarchy = 'created_at'
    fieldsets = [
        (None,               {'fields': ['title']}),
        ('Period:', {'fields': [('active_period', 'is_active')]}),
        ('Tags', {'fields': ['tags']}),
        ('Added by', {'fields': ['created_by']}),
    ]
    list_display = ['title', 'is_active', 'created_by', 'ending_date', 'casted_votes']
    list_filter = ['created_at', 'is_active', 'created_by', 'tags']
    search_fields = ['title']
    actions = [make_inavtive]
    raw_id_fields = ["created_by"]

    inlines = [ChoiceInline]

    def view_on_site(self, ballot):
        """
        Show current Ballot on site.
        :param ballot: Ballot
        :return: Reverse url
        """
        url = reverse('ballot:ballot_details', kwargs={'pk': ballot.pk})
        return url

    def casted_votes(self, ballot):
        """
        Shows total casted votes in a ballot with some html.
        :param ballot: Ballot
        :return: Html
        """
        choices = ballot.choices
        total_casted_votes = sum(choice.votes for choice in choices)
        colored_display = format_html(
            '<strong style="color: #036;">{}</strong>'.format(total_casted_votes)
        )
        return colored_display

    casted_votes.short_description = 'Total Caster Votes'

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


class ChoiceAdmin(admin.ModelAdmin):
    """
    Choice Admin
    """
    list_display = ['text', 'ballot']
    search_fields = ['title', 'ballot']
    raw_id_fields = ["ballot"]


admin.site.register(Ballot, BallotAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Vote)
admin.site.register(Tag)
