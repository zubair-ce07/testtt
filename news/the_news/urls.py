__author__ = 'luqman'


from django.conf.urls import url, include
import views
from decorators import ip_check

app_name = "the_news"
urlpatterns = [
    url(r'^the_news/fetch/(?P<spider_name>[\w-]+)/?$',
        views.FetchView.as_view(),
        name='fetch_news'),
    url(r'^the_news/terminate/(?P<spider_name>[\w-]+)/?$',
        views.TerminateView.as_view(),
        name='terminate_fetch_news'),
    url(r'^the_news/?$',
        views.TheNewsMainView.as_view(),
        name='main'),
    url(r'^news/(?P<page>\d+)/?$|^news/?$',
        views.NewsListView.as_view(),
        name='news_list'),
    url(r'^news/detail/(?P<pk>\d+)/?$',
        views.NewsDetailView.as_view(),
        name='news_detail'),

    # api urls
    url(r'^khabar/?$',
        views.NewsListAPIView.as_view()),
    url(r'^khabar/(?P<pk>\d+)/?$',
        views.NewsDetailsAPIView.as_view()),
]
