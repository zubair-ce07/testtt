from django.contrib import admin
from .models import Post
from .models import Category
from .models import Comment
from .models import LikeComment
from .models import LikePost

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(LikePost)
admin.site.register(LikeComment)

