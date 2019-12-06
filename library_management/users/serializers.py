import logging

from rest_framework import serializers

from authors.models import Author
from publishers.models import Publisher
from utils import regisiter_user

logger = logging.getLogger(__name__)


class AuthorSignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'},
                                      write_only=True)

    class Meta:
        model = Author
        fields = ['first_name', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
        }

    def save(self):
        return regisiter_user(self.validated_data, Author)


class PublisherSignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'},
                                      write_only=True)

    class Meta:
        model = Publisher
        fields = ['company_name', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
            'company_name': {'required': True},
        }

    def save(self):
        return regisiter_user(self.validated_data, Publisher)
