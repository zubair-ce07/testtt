from django.urls import path, include
from rest_framework import routers

from .views import ProductsViewSet, BrandViewSet, CategoryViewSet

app_name = 'products'
router = routers.DefaultRouter()
router.register(r'products', ProductsViewSet)
router.register(r'brands', BrandViewSet)
router.register(r'categories', CategoryViewSet)
urlpatterns = [
    path(r'', include(router.urls)),
]

