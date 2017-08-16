from django.conf.urls import url
from rest_framework.authtoken import views as auth_views

from news.api import views

urlpatterns = [
    url(r'^$', views.NewsList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', views.NewsDetail.as_view()),
    url(r'^api-token-auth/', auth_views.obtain_auth_token),
]
