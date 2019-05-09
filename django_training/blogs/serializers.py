from rest_framework.serializers import ModelSerializer

from blogs.models import Blog


class BlogSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'blog_title', 'blog_description','published_date', 'user_id']
