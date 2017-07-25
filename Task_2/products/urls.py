from django.conf.urls import url

from products import views

app_name = 'products'

urlpatterns = [
    url(r'^create/$', views.CreateProductView.as_view(), name='create-product'),
    url(r'^edit/(?P<pk>\d+)$', views.EditProductView.as_view(), name='edit-product'),
    url(r'^delete/(?P<pk>\d+)$', views.DeleteProductView.as_view(), name='delete-product'),
    url(r'^search/$', views.SearchProductView.as_view(), name='search-product'),
]
