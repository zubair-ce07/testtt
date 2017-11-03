from rest_framework import serializers

from .models import News


class NewsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    author_name = serializers.CharField(source='author.username')
    date = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=200)
    detail = serializers.CharField(max_length=2000)
    link = serializers.URLField(max_length=200)
    image_url = serializers.URLField(max_length=200)

    def create(self, validated_data):
        return News.objects.create(**validated_data)
