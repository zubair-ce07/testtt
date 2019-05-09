from django.urls import path

from apis.views import CreateBlog, BlogList, BlogDetail
from . import views


urlpatterns = [
    path('blogs/', BlogList.as_view(), name='blogs'),
    path('blog/<int:pk>/', BlogDetail.as_view(), name='blog'),
    path('create_blog/', CreateBlog.as_view(), name='create_blog_api'),
    # path('add_blog', views.add_new_blog, name='add_blog'),
    # path('edit_blog/<int:blog_id>', views.edit_blog, name='edit_blog'),
    # path('delete_blog/', views.delete_blog, name='delete_blog'),
]
