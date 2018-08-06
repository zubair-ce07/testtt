from django.urls import path
from articles.views import ArticleList, SearchResults, ArticleDetail

urlpatterns = [
    path('search/', SearchResults.as_view(), name='search'),
    path('articles/', ArticleList.as_view(), name='article-list'),
    path('articles/<int:pk>/', ArticleDetail.as_view(), name='article-detail'),
]
