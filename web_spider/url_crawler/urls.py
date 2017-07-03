from django.conf.urls import url
from url_crawler import views


urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index')
]
