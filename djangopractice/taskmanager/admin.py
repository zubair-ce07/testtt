from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import path, reverse
from django.utils.html import mark_safe, format_html

from taskmanager import views, models, forms


class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'mark_as_completed']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:pk>/status/', views.change_status, name='status'),
        ]
        return custom_urls + urls

    def mark_as_completed(self, obj):
        return format_html(
            '<a class="button" href="{}">Change Status</a>',
            reverse('admin:status', args=[obj.pk]),
        )
    mark_as_completed.short_description = "Status"


class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'full_name', 'total_tasks']
    form = forms.CustomUserChangeForm
    add_form = forms.CustomUserCreationForm
    fieldsets = (('User details', {'fields': ('username', 'first_name', 'last_name', 'email')}),
                 ('Extra', {'fields': ('bio', 'image', 'birth_date')}),)
    add_fieldsets = (('None', {'fields': ('username', 'email', 'password1', 'password2')}),)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        queryset |= self.model.objects.filter(task__title__icontains=search_term)
        use_distinct = True
        return queryset, use_distinct

admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.CustomUser, CustomUserAdmin)