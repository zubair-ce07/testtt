from django.urls import path
from manager.views import Home, AddProduct

urlpatterns = [
    path('', Home.as_view()),
    path('add_product/', AddProduct.as_view()),
]