from django.urls import path
from articles.views import ArticleList, SearchResults, ArticleDetail

urlpatterns = [
    path('', ArticleList.as_view(), name='home-page'),
    path('home/', ArticleList.as_view(), name='articles-list'),
    path('home/search/', SearchResults.as_view(), name='search'),
    path('articles/', ArticleList.as_view(), name='article-list'),
    path('articles/<int:pk>/', ArticleDetail.as_view(), name='article-detail'),
]
