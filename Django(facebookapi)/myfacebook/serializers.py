from rest_framework import serializers
from django.contrib.auth.models import User

from .models import News


class NewsSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(source='author', queryset=User.objects.all())

    class Meta:
        model = News
        fields = ('id', 'author_id', 'author_name', 'title', 'description',
                  'detail', 'link', 'image_url', 'date')
        read_only_fields = ('author_name', 'id')

