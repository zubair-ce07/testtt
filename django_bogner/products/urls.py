from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # /products
    path('', views.IndexView.as_view(), name='index'),
    # /products/category<cat-id>
    path('category<int:pk>/', views.CategoryProducts.as_view(), name='category_products'),
    # /products/p<product-id>
    path('p<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    # path('<str:retailer_sku>', views.ProductDetail.as_view(), name='product_detail'),
]
