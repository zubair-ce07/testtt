from django.contrib import admin
from .models import TodoItem
# Register your models here.
admin.site.register(TodoItem)

class TodoItemAdmin(admin.ModelAdmin):
    fields = ('description', 'status', 'date_created', 'date_completed')
