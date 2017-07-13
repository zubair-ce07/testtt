from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "s_store"

urlpatterns = [
    url(r'^brands/$', views.BrandList.as_view(), name="brands"),
    url(r'^brand/(?P<pk>[0-9]+)/$',
        views.BrandDetails.as_view(), name="brand-detail"),
    url(r'^users/$', views.UserList.as_view(), name="user-list"),
    url(r'^user/(?P<pk>[0-9]+)/$',
        views.UserDetail.as_view(), name="user-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
