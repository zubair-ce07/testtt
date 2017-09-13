from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from articles.models import Articles
from articles.serializers import ArticleSerializer


class ArticleViewSet(ModelViewSet):

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = Articles.objects.all().order_by('-id')
    serializer_class = ArticleSerializer
