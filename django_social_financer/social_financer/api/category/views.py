from rest_framework import generics, permissions

from . import serializers
from accounts.models import Category


class GetCategories(generics.ListAPIView):
    serializer_class = serializers.GetCategoriesSerializer
    queryset = Category.objects.all()
    permission_classes = (permissions.AllowAny,)
