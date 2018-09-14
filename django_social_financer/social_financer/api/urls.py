__author__ = 'abdul'
from django.urls import path, include
from rest_framework.authtoken import views as authviews

from . import views

app_name = 'api'
urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name='login'),
    # Accounts
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/', views.ProfileView.as_view(), name='my_profile'),
    path('consumers_list/', views.UnpairedConsumersList.as_view(), name='consumers_list'),
    path('consumers_list/<int:pk>', views.ConsumerDetail.as_view()),
    path('my_consumers/', views.PairedConsumersList.as_view(), name='my_consumers'),
    path('my_donor/', views.HomeConsumer.as_view(), name='home_consumer'),
    # Feedback
    path('post_feedback/<int:pk>', views.PostFeedbackView.as_view(), name='give_feedback'),
    path('get_feedback/', views.GetFeedbackView.as_view(), name='give_feedback'),
    # Report
    path('admin/view_reports/<int:pk>', views.ViewReports.as_view(), name='view_reports'),
    path('report/<int:pk>', views.PostReportView.as_view(), name='report_user'),
    #Categories
    path('get_categories/', views.GetCategories.as_view(), name='get_categories'),
    path('api-token-auth/', authviews.obtain_auth_token),
]
