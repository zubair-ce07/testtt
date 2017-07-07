from django.contrib import admin

from .models import Feedbacks


class FeedbacksAdmin(admin.ModelAdmin):
    search_fields = ('name', 'comment')
    list_filter = ('department', 'store',)
    list_display = ('name', 'gender',)


admin.site.register(Feedbacks, FeedbacksAdmin)
