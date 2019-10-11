from django.urls import include, path
from rest_framework import routers

from . import views

institute_router = routers.DefaultRouter()
program_router = routers.DefaultRouter()
institute_router.register('campuses', views.CampusViewSet)
institute_router.register('programs', views.ProgramViewSet)
institute_router.register('', views.InstitutionViewSet)
program_router.register('courses', views.CourseViewSet)
# Wire up our API using automatic URL routing.
urlpatterns = [
    path('institutions/<int:institution_id>/', include(institute_router.urls)),
    path('programs/<int:program_id>/', include(program_router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
