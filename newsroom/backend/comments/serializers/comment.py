from rest_framework.serializers import ModelSerializer, SerializerMethodField
from backend.comments.models import Comment


class CommentSerializer(ModelSerializer):
    username = SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('username', 'date', 'content')

    def get_username(self, obj):
        return obj.user.username

    def get_news_source_url(self, obj):
        return obj.news.source_url