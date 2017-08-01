from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "api"

urlpatterns = [
    url(r'^brand/list/$', views.BrandList.as_view(), name="brand-list"),
    url(r'^brand/create/$', views.BrandCreate.as_view(), name="brand-create"),
    url(r'^brand/(?P<pk>[0-9]+)/$',
        views.BrandDetails.as_view(), name="brand-detail"),

    url(r'^users/$', views.UserList.as_view(), name="user-list"),
    url(r'^user/(?P<pk>[0-9]+)/$',
        views.UserDetail.as_view(), name="user-detail"),

    url(r'^products/$', views.ProductList.as_view(), name="product-list"),
    url(r'^product/(?P<pk>[0-9]+)/$', views.ProductDetail.as_view(),
        name="product-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
