from django.urls import path, re_path, include
from rest_framework import routers
from api.tweets import views
from api.tweets.views import upload, api_trends, api_tweets, TrendList

urlpatterns = [
    path('upload', upload, name='upload'),
    path('trends/$', TrendList.as_view(), name='trend_list'),
]
