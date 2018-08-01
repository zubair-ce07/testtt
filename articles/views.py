from rest_framework.views import APIView
from rest_framework.response import Response
from articles.models import Article
from articles.serializers import ArticleSerializer
from rest_framework import generics


class ArticleList(APIView):

    def get(self, request, format=None):
        articles = Article.objects.filter(category="ARTICLE")
        news = Article.objects.filter(category="NEWS")
        response = ArticleSerializer((articles | news), many=True)
        return Response(response.data)


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
