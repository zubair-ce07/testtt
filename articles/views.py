from django.http import HttpResponse
from drf_multiple_model.views import ObjectMultipleModelAPIView
from common.pagination import LimitPagination

from articles.models import Article
from articles.serializers import ArticleSerializer
from rest_framework import generics


def index(request):
    return HttpResponse("Hello, world. You're at the articles index.")


class ArticleList(ObjectMultipleModelAPIView):
    pagination_class = LimitPagination
    querylist = [
        {
            'queryset': Article.objects.filter(category="ARTICLE"),
            'serializer_class': ArticleSerializer,
            'label': 'Articles',
        },
        {
            'queryset': Article.objects.filter(category="NEWS"),
            'serializer_class': ArticleSerializer,
            'label': 'News',
        },
    ]


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
