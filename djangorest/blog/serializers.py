from rest_framework.serializers import ModelSerializer, SlugRelatedField
from blog.models import Blog
from user.models import User


class BlogSerializer(ModelSerializer):
    created_by = SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Blog
        fields = '__all__'
