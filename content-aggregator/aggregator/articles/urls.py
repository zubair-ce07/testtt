from django.urls import path

from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('add-post', views.ArticleForm.as_view(), name='add_article'),
    path('add-author', views.AuthorForm.as_view(), name='add_author'),
    path('add-website', views.WebsiteForm.as_view(), name='add_website'),
]
