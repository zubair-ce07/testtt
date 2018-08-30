from django.conf.urls import url
from fanatics_item import views

urlpatterns = [
    url(r'^fanatics_items/$', views.FanaticsItemList.as_view()),
    url(r'^fanatics_items/(?P<pk>[0-9]+)/$', views.FanaticsItemDetail.as_view()),
]