from django.urls import path, include

from . import views
import feedback.views, report.views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home_view, name='home'),
    path('my_consumers/', views.donors_pairs, name='my_consumers'),

    # path('file_report/<int:pk>', report.views.ReportView.as_view(), name='report_user'),

]