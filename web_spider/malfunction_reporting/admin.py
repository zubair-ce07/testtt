from datetime import date
from django.contrib import admin
from django.utils import timezone
from malfunction_reporting.models import Task, SafetyHazard, Movie, Investigation, SafeActReport


admin.site.site_header = 'Reporter & Crawler admin'
admin.site.index_title = 'site admin'
admin.site.site_title = 'Reporter & Crawler admin'

admin.site.register(SafetyHazard)
admin.site.register(Movie)
admin.site.register(SafeActReport)
admin.site.register(Investigation)


class YearReportedListFilter(admin.SimpleListFilter):
    """
    filter to be used on task list on admin site to show
    tasks of this year or last year
    """
    title = 'Year reported in'

    parameter_name = 'year'

    def lookups(self, request, model_admin):
        year = timezone.now().year
        return (
            (year, 'This Year'),
            (year-1, 'Last year'),
        )

    def queryset(self, request, queryset):
        response = None
        year = timezone.now().year
        if self.value() == str(year):
            response = queryset.filter(created_at__gte=date(year, 1, 1), created_at__lte=date(year, 12, 31))
        elif self.value() == str(year-1):
            response = queryset.filter(created_at__gte=date(year-1, 1, 1), created_at__lte=date(year-1, 12, 31))
        return response


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    overrides default admin site for task model
    """
    date_hierarchy = 'created_at'
    fields = (('priority', 'status',), 'created_at', 'completed_at', 'assignee')
    list_display = ('id', 'assignee', 'status', 'priority', 'is_completed')
    list_display_links = ('id', )
    list_editable = ('status', )
    list_filter = ('status', 'safetyhazard__reported_by', YearReportedListFilter,)
    search_fields = ('^assignee__email', )
    actions = ('make_priority_high', )

    def make_priority_high(self, request, queryset):
        """
        sets priority high for all task in queryset
        and is used as action on task list page

        Arguments:
            request (Request): request object associated
            queryset (QuerySet): contains all selected objects on admin list page
        """
        queryset.update(priority=Task.HIGH)
    make_priority_high.short_description = 'Make Priority High'

    def save_model(self, request, obj, form, change):
        """
        if user is updating status to completed then updates
        completion time too.

        Arguments:
            request (Request): request object associated
            obj (Task): object to be saved
            form (Form): form used on admin site to validate data
            change (Boolean): whether object was created or changed
        """
        try:
            if form.cleaned_data['status'] == Task.COMPLETED:
                obj.completed_at = timezone.now()
        except KeyError:
            pass
        super(TaskAdmin, self).save_model(request, obj, form, change)
