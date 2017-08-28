from rest_framework.serializers import ModelSerializer, SerializerMethodField, Serializer
from backend.comments.models import Comment


class RecursiveField(Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(ModelSerializer):
    username = SerializerMethodField()
    replies = RecursiveField(many=True)

    class Meta:
        model = Comment
        fields = ('id', 'username', 'date', 'content', 'replies')

    def get_username(self, obj):
        return obj.user.username

    def get_news_source_url(self, obj):
        return obj.news.source_url
