from rest_framework.viewsets import ReadOnlyModelViewSet
from backend.news.models import News
from backend.categories.models import Category
from backend.news.serializers.news import NewsSerializer
from backend.categories.serializers.category import CategorySerializer
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'name'

    @detail_route(url_path='news')
    def get_category_news(self, request, name=None):
        category = self.get_object()
        category_news = News.objects.filter(category__name=category.name).order_by('-published_date')
        serializer = NewsSerializer(category_news, many=True)
        return Response(serializer.data)

