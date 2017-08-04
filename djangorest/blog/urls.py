from django.conf.urls import url
from blog.views import APIBlogList, APIBlogDetail


urlpatterns = [
    url(r'^blog/$', APIBlogList.as_view(), name='blog'),
    url(r'^blog/(?P<slug>[a-z_]+)/$', APIBlogDetail.as_view(), name='detail'),
]
