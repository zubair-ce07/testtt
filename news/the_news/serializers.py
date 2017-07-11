__author__ = 'luqman'


from rest_framework import serializers
from the_news.models import News


class NewsSerializer(serializers.ModelSerializer):
    website = serializers.ReadOnlyField(source='news_paper.website')

    class Meta:
        model = News
        fields = ['id', 'title', 'date', 'website']