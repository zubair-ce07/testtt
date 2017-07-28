from django.conf.urls import url
from blog.views import APIBlogList, APIBlogDetail


urlpatterns = [
    url(r'^blog/$', APIBlogList.as_view(), name='blog'),
    url(r'^blog/(?P<pk>[0-9]+)/$', APIBlogDetail.as_view(), name='detail'),
]
