from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.HomepageView, name='index'),
    path('upload/', views.UploadsView.as_view(), name='upload'),
    path('my_uploads/', views.MyUploadsView, name='my_uploads'),
    path('delete_image/', views.DeleteImageView, name='delete_image'),
]
