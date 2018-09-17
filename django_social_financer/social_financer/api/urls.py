__author__ = 'abdul'
from django.urls import path, include

app_name = 'api'
urlpatterns = [
    path('accounts/', include('api.accounts.urls')),
    path('categories/', include('api.category.urls')),
    path('feedback/', include('api.feedback.urls')),
    path('report/', include('api.report.urls')),
]
