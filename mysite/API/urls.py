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

    url(r'^product/list/$', views.ProductList.as_view(), name="product-list"),
    url(r'^product/create/$', views.ProductCreate.as_view(), name="product-create"),
    url(r'^product/(?P<pk>[0-9]+)/$', views.ProductDetail.as_view(),
        name="product-detail"),

    # url(r'^images/$', views.ImageList.as_view(), name="images"),
    # url(r'^image/(?P<pk>[0-9]+)/$',
    #     views.ImageDetial.as_view(), name="image-detail"),

    # url(r'^skus/$', views.SkuList.as_view(), name="skus"),
    # url(r'^sku/(?P<pk>[0-9]+)/$',
    #     views.SkuDetail.as_view(), name="sku-detail"),


]

urlpatterns = format_suffix_patterns(urlpatterns)
