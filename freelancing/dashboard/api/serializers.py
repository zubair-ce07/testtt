from rest_framework import serializers

from accounts.models import User
from ..models import Requests, RequestFiles
from seller.api.serializers import CategorySerializer
from seller.models import Category


class RequestFilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequestFiles
        fields = (
            'id',
            'file_name'
        )


class RequestSerializer(serializers.ModelSerializer):
    request_files = RequestFilesSerializer(read_only=True, many=True)
    categories = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = Requests
        fields = (
            'id',
            'description',
            'date',
            'duration',
            'budget',
            'request_files',
            'categories'
        )

    def create(self, validated_data):
        request = self.context.get("request")
        if request.user.is_anonymous:
            raise serializers.ValidationError(
                "User not logged in"
            )
        # request_files = validated_data.pop('request_files')
        categories = request.data.get('categories', [])
        print("CATERGORIES", categories)
        buyer_request = Requests.objects.create(
            buyer=request.user, **validated_data
        )
        for category in categories:
            category = Category.objects.get(id=category["id"])
            buyer_request.categories.add(category)

        return buyer_request
