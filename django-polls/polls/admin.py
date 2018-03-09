from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import Choice, Question

# Register your models here.
@admin.register(Choice)
class AuthorAdmin(admin.ModelAdmin):
    fields = ('question', 'choice_text', 'votes')
    
    list_display = ('question','choice_text','votes')
    list_filter = ['choice_text']
    


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes':['collapse']}),
    ]
    inlines = [ChoiceInLine]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']


# class OptionFilter(SimpleListFilter):
#     title = 'choice'
#     parameter_name = 'votes'

#     def lookup(self, request, ModelAdmin):
#         votes = set([Choice.votes for model in model.objects.all()])
#         # return [(model.question, model.votes for c in votes)] 
#         return votes

#     def queryset(self, request, queryset):
#         if self.value():
#             return queryset.filter(self.value())
#         else:
#             return queryset
       
admin.site.unregister(Choice)
admin.site.register(Choice, AuthorAdmin)
admin.site.register(Question, QuestionAdmin)


