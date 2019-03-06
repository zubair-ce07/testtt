from rest_framework import serializers
from rest_framework.fields import Field

from api.tweets.models import Trends, Tweets


class TweetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tweets
        fields = '__all__'


class TrendSerializer(serializers.ModelSerializer):
    tweets = TweetSerializer(many=True, required=False)

    class Meta:
        model = Trends
        fields = ('__all__')

