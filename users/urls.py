from django.urls import path
from .views import SignUpView, ShowProducts, OrderProducts

urlpatterns = [
    path('', ShowProducts.as_view(), name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('order/', OrderProducts.as_view(), name='order'),
]