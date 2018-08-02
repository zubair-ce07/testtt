from rest_framework.views import APIView
from rest_framework.response import Response
from articles.models import Article
from articles.serializers import ArticleDetailSerializer, GetAllArticlesSerializer, SearchSerializer
from rest_framework import generics


class ArticleList(APIView):

    def get(self, request, format=None):

        serializer = GetAllArticlesSerializer(data={})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer


class SearchResults(APIView):

    def get(self, request, format=None):

        serializer = SearchSerializer(data={}, context={'search': request.query_params.get('q', '')})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
