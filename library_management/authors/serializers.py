import logging

from rest_framework import serializers

from .models import Author

logger = logging.getLogger(__name__)


class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Author
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone',
        ]


class CustomAuthorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = [
            'id', 'full_name'
        ]

    def get_full_name(self, obj):
        return obj.get_full_name()
