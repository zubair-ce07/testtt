from django.urls import path

from apis.views import CreateBlog, BlogList, BlogDetail


urlpatterns = [
    path('blogs/', BlogList.as_view(), name='blogs'),
    path('blog/<int:pk>/', BlogDetail.as_view(), name='blog'),
    path('create_blog/', CreateBlog.as_view(), name='create_blog_api'),
]
