from django.conf.urls import url
from movies.views import index

urlpatterns = [
    url(r'^$', index),
]
