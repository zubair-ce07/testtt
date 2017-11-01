from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models import Count

from .models import UserFollowers, UserStatus, News, UserProfile

admin.site.register(UserFollowers)
admin.site.register(UserStatus)
admin.site.register(UserProfile)


# class NewsAuthorListFilter(SimpleListFilter):
#     title = 'Authors'
#
#     # Parameter for the filter that will be used in the URL query.
#     parameter_name = 'author'
#
#     def lookups(self, request, model_admin):
#         return (
#             ('yes', 'Experts'),
#             ('no', 'Newbies'),
#         )
#
#     def queryset(self, request, queryset):
#
#         if self.value() == 'yes':
#             return queryset.annotate(num_author=Count('author')).all()
#         if self.value() == 'no':
#             return queryset.filter(author__count__lte=3)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'date', )
    search_fields = ('author__username', )
