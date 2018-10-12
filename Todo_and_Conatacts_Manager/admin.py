from django.contrib import admin
from django.contrib.auth import get_user_model

from system.models import Contact, Todo, Item


User = get_user_model()


class ItemInline(admin.StackedInline):
    model = Item


class TodoAdmin(admin.ModelAdmin):
    inlines = [ItemInline]
    list_display = ['title', 'user']


class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_number',  'user']


admin.site.register(User)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Todo, TodoAdmin)
