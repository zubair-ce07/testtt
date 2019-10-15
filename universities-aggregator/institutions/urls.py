from django.urls import include, path, re_path
from rest_framework import routers

from . import views

institute_router = routers.DefaultRouter()
institute_router.register('campuses', views.CampusViewSet)
institute_router.register('programs', views.ProgramViewSet)
institute_router.register('semester', views.SemesterViewSet)
institute_router.register('', views.InstitutionViewSet)

program_router = routers.DefaultRouter()
program_router.register('courses', views.CourseViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('institutions/', include(institute_router.urls)),
    re_path(r'^institutions/(?P<institution_id>[0-9])/', include(institute_router.urls)),
    re_path(r'^programs/(?P<program_id>[0-9])/', include(program_router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
