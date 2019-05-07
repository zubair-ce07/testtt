from django.urls import path

from . import views

urlpatterns = [
    path('add_blog', views.add_new_blog, name='add_blog'),
    path('edit_blog/<int:blog_id>', views.edit_blog, name='edit_blog'),
    path('delete_blog/', views.delete_blog, name='delete_blog'),
]