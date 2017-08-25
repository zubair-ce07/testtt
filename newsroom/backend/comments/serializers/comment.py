from rest_framework.serializers import ModelSerializer, SerializerMethodField
from backend.comments.models import Comment
from backend.users.serializers.user import UserSerializer
from backend.news.serializers.news import NewsSerializer


class CommentSerializer(ModelSerializer):
    news_source_url = SerializerMethodField()
    username = SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('username', 'news_source_url', 'content')

    def get_username(self, obj):
        return obj.user.username

    def get_news_source_url(self, obj):
        return obj.news.source_url