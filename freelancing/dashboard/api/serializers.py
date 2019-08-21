from rest_framework import serializers, status
from rest_framework.response import Response
from django.http import JsonResponse

from accounts.models import User
from ..models import Requests, RequestFiles
from seller.api.serializers import CategorySerializer
from seller.models import Category


class RequestFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequestFiles
        fields = (
            'id',
            'file_name'
        )


class RequestFilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequestFiles
        lookup_field = 'id'
        fields = (
            'id',
            'file_name'
        )

    def create(self, validated_data):
        request = self.context.get("request")
        if request.user.is_anonymous:
            raise serializers.ValidationError(
                "User not logged in"
            )
        buyer_request_id = request.data.get("buyer_request_id")
        if not buyer_request_id:
            raise serializers.ValidationError(
                "KeyMissing: buyer_request_id"
            )

        buyer_request = Requests.objects.get(id=buyer_request_id)
        request_files = []
        for uploaded_file in request.data.getlist('files'):
            request_file = RequestFiles.objects.create(
                request=buyer_request,
                file_name=uploaded_file
            )
            request_file.save()
            request_files.append(request_file)
        #: FIXME return multiple objects. currently returning {} on post
        return RequestFiles.objects.all().get(request=buyer_request)


class RequestSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="category_name"
    )
    buyer = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = Requests
        fields = (
            'id',
            'description',
            'date',
            'duration',
            'budget',
            'categories',
            'buyer'
        )

    def create(self, validated_data):
        request = self.context.get("request")
        if request.user.is_anonymous:
            raise serializers.ValidationError(
                "User not logged in"
            )
        # request_files = validated_data.pop('request_files')
        categories = request.data.get('categories', [])
        buyer_request = Requests.objects.create(
            buyer=request.user, **validated_data
        )
        for category in categories:
            category = Category.objects.get(id=category["id"])
            buyer_request.categories.add(category)

        return buyer_request
