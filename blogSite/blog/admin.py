from django.contrib import admin
from .models import Post
from .models import Category
from .models import Comment
from .models import LikeComment
from .models import LikePost


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category_name')
    list_filter = ('author', 'category__category')

    def category_name(self, post):
        return post.category.category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('body', 'user', 'post_name')
    list_filter = ('user', 'post__title')

    def post_name(self, comment):
        return comment.post.title


class LikePostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_name', 'vote')
    list_filter = ('user', 'post__title',)

    def post_name(self, like):
        return like.post.title

class LikeCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment_id', 'vote')
    list_filter = ('user', 'comment__id')


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(LikePost, LikePostAdmin)
admin.site.register(LikeComment, LikeCommentAdmin)

