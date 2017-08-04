from django.conf.urls import url

from news import views

urlpatterns = [
    url(r'^$', views.NewsView.as_view(), name='news'),
    url(r'^(?P<pk>[\d]+)/$', views.NewsDetailedView.as_view(), name='news_detailed'),
]
