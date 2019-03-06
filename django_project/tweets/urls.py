from django.urls import path, re_path, include
from rest_framework import routers
from api.tweets import views
from api.tweets.views import upload, api_trends, api_tweets, TrendList

urlpatterns = [
    re_path('upload', upload, name='upload'),
    # re_path('api_trends', api_trends, name='api_trends'),
    # re_path('api_tweets', api_tweets, name='api_tweets'),
    re_path('trends/$', TrendList.as_view(), name='trend_list'),



]