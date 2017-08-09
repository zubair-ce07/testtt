from django.conf.urls import include, url

from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from . import views


urlpatterns = [
    url(r'^employees/$', views.EmployeeListAPIView.as_view(),
        name='employee-list'),
    url(r'^employees/(?P<username>\w+)/$', views.EmployeeRetrieveAPIView.as_view(),
        name='employee-detail',),
    url(r'^employees/(?P<username>\w+)/directs/?$',
        views.EmployeeDirectsView.as_view(), name="directs"),
    url(r'^employees/(?P<username>\w+)/appraisals/?$',
        views.AppraisalView.as_view(), name="appraisals"),
    url(r'^employees/(?P<username>\w+)/appraisals/create/?$',
        views.AppraisalCreateAPIView.as_view(), name="appraisals-create"),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^obtain-auth-token/$', obtain_auth_token)
]
