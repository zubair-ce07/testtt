from django.shortcuts import render
from django.http import HttpResponse
from users.models import Profile
from users.serializers import UserSerializer
from rest_framework import viewsets


def index(request):
    return HttpResponse("Hello, world. You're at the users index.")
