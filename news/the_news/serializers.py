__author__ = 'luqman'


from rest_framework import serializers
from the_news.models import News
from django.contrib.auth.models import User


class NewsSerializer(serializers.ModelSerializer):
    website = serializers.ReadOnlyField(source='news_paper.website')

    class Meta:
        model = News
        fields = ['id', 'title', 'date', 'website']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')
