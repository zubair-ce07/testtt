__author__ = 'abdul'
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/view_reports/<int:pk>', views.ViewReports.as_view(), name='view_reports'),
    path('report/', views.PostReportView.as_view(), name='report_user'),
]
