from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from rest_framework.generics import ListCreateAPIView

from . import views
from .models import Product
from .serializers import ProductSerializer

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', LogoutView.as_view(template_name='registration/base.html'), name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^home$', views.home, name='home'),
    url(
        r'^product',
        ListCreateAPIView.as_view(queryset=Product.objects.all(), serializer_class=ProductSerializer),
        name='product'
    )
]

