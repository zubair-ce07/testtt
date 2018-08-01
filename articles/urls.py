from django.urls import path
from django.conf.urls import url

from articles.views import ArticleList
from . import views

urlpatterns = [
    path('', ArticleList.as_view()),
]
