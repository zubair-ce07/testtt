from django.conf.urls import url

from .views import show_profile

app_name = 'users'

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', show_profile),
]
