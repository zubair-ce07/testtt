from rest_framework.serializers import ModelSerializer
from backend.news.models import NewsSource


class NewsSourceSerializer(ModelSerializer):

    class Meta:
        model = NewsSource
        fields = ('id', 'name', )
