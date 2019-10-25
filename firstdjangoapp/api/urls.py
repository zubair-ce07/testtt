from django.conf.urls import url

from .views import OptionsList, ProductDetail, ProductList, UserDetail, UserList

urlpatterns = [
    url(r'^products/(?P<retailer_sku>[-\w]+)/', ProductDetail.as_view(), name='product_detail'),
    url(r'^products/', ProductList.as_view(), name='product_list'),
    url(r'^users/(?P<username>[\w]+)/', UserDetail.as_view(), name='user_detail'),
    url(r'^users/', UserList.as_view(), name='user_list'),
    url(r'^options/', OptionsList.as_view(), name='search_options')
]
