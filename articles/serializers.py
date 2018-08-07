from rest_framework import serializers
from articles.models import Article, ArticleChoices
from teams.models import Player, Team
from teams.serializers import PlayerSerializer, TeamSerializer


class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class GetAllArticlesSerializer(serializers.Serializer):
    articles = serializers.SerializerMethodField()
    news = serializers.SerializerMethodField()

    def get_articles(self, obj):
        queryset = Article.objects.filter(category=ArticleChoices.ARTICLE)
        return ArticleDetailSerializer(instance=queryset, many=True).data

    def get_news(self, obj):
        queryset = Article.objects.filter(category=ArticleChoices.NEWS)
        return ArticleDetailSerializer(instance=queryset, many=True).data


class SearchSerializer(serializers.Serializer):
    players = serializers.SerializerMethodField()
    articles = serializers.SerializerMethodField()
    teams = serializers.SerializerMethodField()

    def get_players(self, obj):
        queryset = Player.objects.filter(name__icontains=self.context.get('search'))
        return PlayerSerializer(instance=queryset, many=True).data

    def get_teams(self, obj):
        queryset = Team.objects.filter(name__icontains=self.context.get('search'))
        return TeamSerializer(instance=queryset, many=True).data

    def get_articles(self, obj):
        queryset = Article.objects.filter(title__icontains=self.context.get('search'))
        return ArticleDetailSerializer(instance=queryset, many=True).data
