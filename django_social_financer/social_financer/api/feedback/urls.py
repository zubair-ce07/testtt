__author__ = 'abdul'
from django.urls import path, include

from . import views

urlpatterns = [
    path('post_feedback/', views.PostFeedbackView.as_view(), name='give_feedback'),
    path('get_feedback/', views.GetFeedbackView.as_view(), name='give_feedback'),
]
