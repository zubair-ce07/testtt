from django.conf.urls import include, url

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'employees', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^employees/(?P<pk>[0-9]+)/directs$',
        views.UserDirectsView.as_view(), name="heirarchy"),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
