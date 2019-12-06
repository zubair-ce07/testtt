from django.contrib import admin

from .models import Publisher


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Account Info', {'fields': ['username', ]}),
        ('Info', {'fields': ['company_name', ]}),
        ('Contact', {'fields': ['phone', 'email', 'website', 'address']}),
    ]
    list_display = ['id', 'username', 'company_name']
