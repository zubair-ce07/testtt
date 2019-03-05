from django.contrib import admin

from web.issue.forms import IssueForm
from web.issue.models import Comment, Issue


class IssueAdmin(admin.ModelAdmin):
    search_fields = ['title', 'created_by', 'manage_by']
    form = IssueForm
    list_display = ['title', 'status', 'priority', 'created_at']
    list_filter = ['title']

    fieldsets = (
        ('Basic', {'fields': ['title', 'description', 'image']}),
        ('User Settings', {'fields': ['created_by', 'manage_by', 'assigned_at', 'resolved_at']}),
        ('Other Details', {'fields': ['status', 'priority']}),
    )

    add_fieldsets = [
        (None, {
            'classes': ('wide',),
            'fields': ('title', 'description', 'priority', 'status')}
         ),
    ]
    ordering = ['created_at']
    filter_horizontal = ()


class CommentAdmin(admin.ModelAdmin):
    search_fields = ['comment', 'comment_by', 'issue']
    list_display = ['comment', 'comment_by', 'issue', 'timestamp']
    list_filter = ['comment', 'timestamp']

    fieldsets = (
        ('Comment', {'fields': ['comment']}),
        ('Comment Settings', {'fields': ['comment_by', 'issue_id']}),
    )

    ordering = ['timestamp']
    filter_horizontal = ()


admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
