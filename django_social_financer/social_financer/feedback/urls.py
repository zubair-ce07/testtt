__author__ = 'abdul'

from django.urls import path, include

from . import views
import accounts.views

app_name = 'feedback'
urlpatterns = [
    path('<int:pk>', views.FeedbackView.as_view(), name='give_feedback'),
]
