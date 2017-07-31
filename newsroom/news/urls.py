from django.conf.urls import url

from news.views import FetchView, NewsMainView, TerminateView

urlpatterns = [
    url(r'^home/?$', NewsMainView.as_view(), name='home'),
    url(r'^fetch/?$', FetchView.as_view(), name='fetch'),
    url(r'^terminate/?$', TerminateView.as_view(), name='terminate'),
]
