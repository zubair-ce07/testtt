from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^brands/$', views.BrandList.as_view(), name="brands"),
]
