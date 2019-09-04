from rest_framework_simplejwt import serializers as jwt_serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from core import models


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = '__all__'


class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PostMedia
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = '__all__'
