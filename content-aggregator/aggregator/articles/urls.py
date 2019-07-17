from django.urls import path

from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.index, name='index'),
    path('add-post', views.PostForm.as_view(), name='add_post'),
    path('<int:article_id>/', views.detail, name='detail')
]
