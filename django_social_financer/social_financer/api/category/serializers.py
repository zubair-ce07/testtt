__author__ = 'abdul'
from datetime import datetime

from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core import serializers as django_serializers
from rest_framework.authtoken.models import Token

from accounts.models import UserProfile, Category
from accounts.helpers import get_user_rating
from feedback.models import Feedback
from report.models import Report


class GetCategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
