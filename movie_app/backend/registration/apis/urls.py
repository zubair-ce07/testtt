from django.urls import path

from . import views

app_name = 'apis'
urlpatterns = [
    path('login', views.login),
    path('signup', views.signup),
    path('logout', views.logout)
]

