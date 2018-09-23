from django.urls import path, include
from django.views.generic import RedirectView
from system.views import UserRudView, UserAPIView,\
    AppraisalAPIView, AppraisalRudView


urlpatterns = [
    path('api/rest-auth/',
         include('rest_auth.urls'), name='login'),
    path('api/user/<int:pk>',
         UserRudView.as_view(), name='user-rud'),
    path('api/user/',
         UserAPIView.as_view(), name='user-list'),
    path('api/appraisals/',
         AppraisalAPIView.as_view(), name='appraisal-list'),
    path('api/appraisals/<int:pk>',
         AppraisalRudView.as_view(), name='aprpaisal-rud')
]
