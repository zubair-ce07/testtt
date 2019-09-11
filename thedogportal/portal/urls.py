from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.homepage, name='index'),
    path('upload/', views.UploadsView.as_view(), name='upload'),
    path('my_uploads/', views.MyUploadsView.as_view(), name='my_uploads'),
]
