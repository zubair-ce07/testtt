from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.index, name='index'),
    path('profile/', include('django.contrib.auth.urls')),
]
