from django.conf.urls import include, url

from rest_framework import routers

from . import views

employee_detail = views.EmployeeViewSet.as_view({
    'get': 'retrieve'
})

router = routers.DefaultRouter()
router.register(r'employees', views.EmployeeViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^employees/(?P<pk>[0-9]+)/$',
        employee_detail, name='employee-detail'),
    url(r'^employees/(?P<pk>[0-9]+)/directs$',
        views.EmployeeDirectsView.as_view(), name="directs"),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
