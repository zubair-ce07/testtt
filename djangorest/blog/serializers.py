from rest_framework.serializers import ModelSerializer
from blog.models import Blog
from user.serializers import UserSerializer


class BlogSerializer(ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = '__all__'
