from rest_framework.viewsets import ReadOnlyModelViewSet
from backend.news.models import News
from backend.categories.models import Category
from backend.news.serializers.news import NewsSerializer
from rest_framework.decorators import list_route
from rest_framework.response import Response
from django.db.models import Q


class NewsViewSet(ReadOnlyModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    @list_route(url_path='top')
    def get_top_news(self, request):
        limit = int(request.GET.get('limit', 1))
        recent_news = News.objects.order_by('-published_date')[:limit]
        serializer = NewsSerializer(recent_news, many=True)
        return Response(serializer.data)

    @list_route(url_path='categories')
    def get_news_categories(self, request):
        limit = int(request.GET.get('limit', 1))
        categories = Category.objects.all()
        categories_news = []
        for category in categories:
            categories_news += News.objects.filter(category__name=category).order_by('-published_date')[:limit]
        serializer = NewsSerializer(categories_news, many=True)
        return Response(serializer.data)

    @list_route(url_path='search')
    def get_search_news(self, request):
        search_string = request.GET.get('query', "")
        keywords = search_string.split('+')
        queries = [Q(detail__icontains=keyword) for keyword in keywords]
        query = queries.pop()
        for condition in queries:
            query |= condition
        searched_news = News.objects.filter(query).order_by('-published_date')
        serializer = NewsSerializer(searched_news, many=True)
        return Response(serializer.data)

