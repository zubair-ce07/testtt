from rest_framework.serializers import ModelSerializer
from user.serializers import UserSerializer
from comment.models import Comment
from blog.serializers import BlogSerializer


class CommentSerializer(ModelSerializer):

    comment_for = BlogSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
