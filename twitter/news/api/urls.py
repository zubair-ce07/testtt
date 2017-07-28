from django.conf.urls import url
from news.api import views

urlpatterns = [
    url(r'^$', views.NewsList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', views.NewsDetail.as_view()),
]
