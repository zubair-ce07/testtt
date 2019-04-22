from django.urls import path

from . import views

urlpatterns = [
    path('data', views.list, name='data'),
    path('signup', views.blog_page, name='first_page'),
    path('home', views.blog_homepage, name='home'),
    path('login', views.blog_login, name='login'),
    path('delete/<int:id>/', views.delete, name='delete'),
]