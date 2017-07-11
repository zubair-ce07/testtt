
from django.conf.urls import url
from . import views


app_name = "super_store"
urlpatterns = [
    # url(r'^$', views.display_data, name="home"),
    url(r'^brands/$', views.BrandListView.as_view(), name="brands"),
    url(r'^products/$', views.ProductsListView.as_view(), name="all-products"),
    url(r'^brands/(?P<name>[a-zA-Z0-9_]+)/$',
        views.ListBrandProductsView.as_view(),
        name="brand-products-list"),
    url(r'^products/(?P<pk>[0-9]+)$', views.ProductDetailView.as_view(),
        name="product-detail"),
]
