from rest_framework.serializers import ModelSerializer, SlugRelatedField
from blog.models import Blog


class BlogSerializer(ModelSerializer):
    created_by = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Blog
        fields = '__all__'
