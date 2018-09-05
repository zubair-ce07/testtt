from django.conf.urls import url
from fanatics_item import views
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.index),
    url('^start_spider/$', views.start_fanatics_spider),
    url('^stop_spider/$', views.stop_fanatics_spider),
    url(r'^fanatics_items/$', views.FanaticsItemList.as_view()),
    url(r'^fanatics_items/(?P<pk>[0-9]+)/$', views.FanaticsItemDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
