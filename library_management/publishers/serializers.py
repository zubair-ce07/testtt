import logging

from rest_framework import serializers

from .models import Publisher

logger = logging.getLogger(__name__)


class PublisherSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Publisher
        fields = [
            'id', 'company_name', 'email', 'address', 'website', 'phone',
        ]


class CustomPublisherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publisher
        fields = [
            'id', 'company_name'
        ]
