from rest_framework import serializers
from articles.models import Article, ArticleChoices


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'author', 'description', 'category', 'url', 'content', 'players', 'teams')
