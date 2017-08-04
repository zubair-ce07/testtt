from rest_framework.serializers import ModelSerializer, SlugRelatedField
from comment.models import Comment
from user.models import User
from blog.models import Blog


class CommentSerializer(ModelSerializer):
    created_by = SlugRelatedField(slug_field='username', queryset=User.objects.all())
    comment_for = SlugRelatedField(slug_field='title', queryset=Blog.objects.all())

    class Meta:
        model = Comment
        fields = '__all__'
