from rest_framework.serializers import ModelSerializer
from backend.news.models import News
from backend.news.serializers.newspaper import NewspaperSerializer
from backend.news.serializers.news_source import NewsSourceSerializer
from backend.categories.serializers.category import CategorySerializer


class NewsSerializer(ModelSerializer):
    category = CategorySerializer()
    news_source = NewsSourceSerializer()
    newspaper = NewspaperSerializer()

    class Meta:
        model = News
        fields = ('id', 'title', 'source_url',
                  'image_url', 'published_date', 'scraped_date',
                  'abstract', 'detail', 'summary',
                  'category', 'news_source', 'newspaper')
