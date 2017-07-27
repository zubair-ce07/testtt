from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from news import views

urlpatterns = [
    url(r'^api/',include('news.api.urls')),
    url(r'^$', login_required()(views.NewsView.as_view()), name='news'),
    url(r'^(?P<pk>[\d]+)/$', login_required()(views.NewsDetailedView.as_view()), name='news_detailed'),
]
