from django.conf.urls import url

from backend.news.views.scrapper import FetchView, NewsMainView, TerminateView

app_name = 'news'
urlpatterns = [
    url(r'^home/?$', NewsMainView.as_view(), name='home'),
    url(r'^fetch/?$', FetchView.as_view(), name='fetch'),
    url(r'^terminate/?$', TerminateView.as_view(), name='terminate'),
]
