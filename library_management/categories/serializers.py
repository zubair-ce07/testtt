import logging

from rest_framework import serializers

from .models import Category

logger = logging.getLogger(__name__)


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Category
        fields = [
            'id', 'name',
        ]
