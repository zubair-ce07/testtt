from django.contrib import admin
from .models import TodoItem


class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'status', 'date_created',
                    'date_completed', 'user',)
    search_fields = ['user__username', 'user__id']
    list_filter = ('status', 'date_created', 'date_completed',)

admin.site.register(TodoItem, TodoItemAdmin)
