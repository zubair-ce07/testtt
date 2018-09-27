from django.urls import path, include
from system.views import UserAPIView, AppraisalAPIView


urlpatterns = [

    path('api/rest-auth/',
         include('rest_auth.urls'), name='login'),
    path('api/user/<int:pk>',
         UserAPIView.as_view(), name='user-rud'),
    path('api/user/',
         UserAPIView.as_view(), name='user-list'),
    path('api/appraisals/',
         AppraisalAPIView.as_view(), name='appraisal-list'),
    path('api/appraisals/<int:pk>',
         AppraisalAPIView.as_view(), name='aprpaisal-rud'),
]
