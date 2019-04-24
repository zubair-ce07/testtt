from django.urls import path

from . import views

urlpatterns = [
    path('blogs_detail', views.get_and_post_blogs, name='blogs_detail'),
    path('signup', views.blog_page, name='first_page'),
    path('login', views.blog_login, name='login'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('edit/<int:id>/', views.edit, name='edit'),

]