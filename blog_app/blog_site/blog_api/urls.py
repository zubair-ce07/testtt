from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers
from rest_framework.documentation import include_docs_urls

from . import views


router = routers.DefaultRouter()
router.register(r'post', views.BlogViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^docs/', include_docs_urls(title='Blog API')),
]
