from fanatics_item.models import FanaticsItem
from rest_framework import serializers


class FanaticsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FanaticsItem
        fields = (
            'product_id', 'breadcrumb', 'title', 'brand',
            'categories', 'description', 'details', 'gender',
            'product_url', 'image_urls', 'price', 'currency',
            'language', 'skus'
        )
