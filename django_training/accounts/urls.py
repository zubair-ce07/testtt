from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('handle_login', views.handle_login, name='handle_login')
]