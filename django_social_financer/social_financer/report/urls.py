__author__ = 'abdul'
from django.urls import path, include

from . import views

app_name = 'report'
urlpatterns = [
    path('<int:pk>', views.ReportView.as_view(), name='report_user'),
]
