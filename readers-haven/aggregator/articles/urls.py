from django.urls import path

from . import views

app_name = 'articles'
urlpatterns = [
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('category/<str:category>/', views.IndexView.as_view(), name='category'),
    path('add-article/', views.ArticleCreateView.as_view(), name='add_article'),
    path('add-author/', views.AuthorCreateView.as_view(), name='add_author'),
    path('add-website/', views.WebsiteCreateView.as_view(), name='add_website'),
    # path('<int:article_id>/comment/', views.comment, name='comment'),
]
