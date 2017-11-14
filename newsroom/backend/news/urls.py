from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from backend.news.views.scrapper import FetchView, NewsMainView, TerminateView
from backend.news.views.news import NewsViewSet

app_name = 'news'

router = DefaultRouter()
router.register(r'news', NewsViewSet)

urlpatterns = [
    url(r'^home/?$', NewsMainView.as_view(), name='home'),
    url(r'^fetch/?$', FetchView.as_view(), name='fetch'),
    url(r'^terminate/?$', TerminateView.as_view(), name='terminate'),
]
urlpatterns += router.urls
