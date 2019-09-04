from django.conf.urls import url

from .views import FileUpload, ProductSearch, ViewAllProducts, ViewResults, ViewProduct


urlpatterns = [
    url(r'^$', ViewAllProducts.as_view(), name="view_all_products"),
    url(r'^upload/', FileUpload.as_view(), name='upload_file'),
    url(r'^search/', ProductSearch.as_view(), name='product_search'),
    url(r'^filterproducts/', ViewResults.as_view(), name="view_brand_results"),
    url(r'^products/', ViewProduct.as_view(), name="view_product"),
]
