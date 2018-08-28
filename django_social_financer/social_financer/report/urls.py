__author__ = 'abdul'
from django.urls import path, include

from . import views

app_name = 'report'
urlpatterns = [
    path('admin/view_reports/<int:pk>', views.ViewReports.as_view(), name='view_reports'),
    path('<int:pk>', views.ReportView.as_view(), name='report_user'),
]
