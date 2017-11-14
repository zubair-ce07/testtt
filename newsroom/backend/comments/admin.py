from django.contrib import admin
from backend.comments.models import Comment


# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_filter = ("user",)

admin.site.register(Comment, CommentAdmin)
