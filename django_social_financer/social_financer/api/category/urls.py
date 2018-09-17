__author__ = 'abdul'
from django.urls import path, include

from . import views

urlpatterns = [
    path('get_categories/', views.GetCategories.as_view(), name='get_categories'),
]
