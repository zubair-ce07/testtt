from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('category<int:pk>/', views.CategoryProducts.as_view(), name='category_products'),
    path('p<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
]
