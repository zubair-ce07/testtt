from django.conf.urls import url
from blog.views import APIBlogList, APIBlogDetailUpdateDelete, APIUserAllBlogList


urlpatterns = [
    url(r'^$', APIBlogList.as_view(), name='blog_list'),
    url(r'^(?P<slug>[a-z-]+)/$', APIBlogDetailUpdateDelete.as_view(), name='detail'),
    url(r'^(?P<username>[a-z_]+)/$', APIUserAllBlogList.as_view(), name='user_blog')
]
