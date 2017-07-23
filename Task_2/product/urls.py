from django.conf.urls import url

from product import views

app_name = 'product'

urlpatterns = [
    url(r'^create/$', views.CreateProductView.as_view(), name='create'),
]