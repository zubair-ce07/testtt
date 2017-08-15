# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Blog
from .serializers import BlogSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50


class BlogViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows blog_api posts to be
    viewed / edited / deleted.
    """
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    pagination_class = StandardResultsSetPagination
