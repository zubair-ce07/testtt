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


class RequestSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="category_name"
    )
    buyer = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    request_files = RequestFileSerializer(read_only=True, many=True)

    class Meta:
        model = Requests
        fields = (
            'id',
            'description',
            'date',
            'duration',
            'budget',
            'categories',
            'buyer',
            'request_files'
        )
