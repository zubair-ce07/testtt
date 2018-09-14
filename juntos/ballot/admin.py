from django.contrib import admin
from .models import Question, Choice, Answer, Tag


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title']}),
        ('Valid period', {'fields': ['start_date', 'end_date']}),
        ('Tags', {'fields': ['tags']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('title', 'start_date', 'created_by')
    list_filter = ['start_date']
    search_fields = ['title']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Answer)
admin.site.register(Tag)
