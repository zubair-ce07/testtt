from django.urls import include, path
from rest_framework import routers
from . import views
from rest_framework import filters

router = routers.DefaultRouter()
# url(r'^users/(?P<user_id>\d+)/$', 'viewname', name='urlname')
router.register('degree-programs', views.ProgramViewSet)
router.register('programs', views.CourseViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
