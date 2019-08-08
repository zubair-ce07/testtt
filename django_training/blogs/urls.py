from django.urls import path

from . import views

urlpatterns = [
    path('add_blog', views.BlogCreate.as_view(), name='create_blog'),
    path('update_blog/<int:pk>', views.UpdateBlog.as_view(), name='update_blog'),
]