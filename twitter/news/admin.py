from django.contrib import admin

from news.models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('title', 'content',)}),
        ('Media', {'fields': ('image',)})
    )

    def save_model(self, request, obj, form, change):
        obj.publisher = request.user
        super(NewsAdmin, self).save_model(request, obj, form, change)
