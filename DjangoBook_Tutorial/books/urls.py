from django.conf.urls import url
from .import views

urlpatterns = [
    url(r'^search-form/', views.search_form, name='search-form'),
]
