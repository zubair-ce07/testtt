from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from articles.models import Article
from articles.serializers import ArticleSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import action


def index(request):
    return HttpResponse("Hello, world. You're at the articles index.")

