from django.conf.urls import url, include

urlpatterns = [
    url(r'^news/', include('news.api.urls')),
]
