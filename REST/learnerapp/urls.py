from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from learnerapp import views


router = DefaultRouter()
router.register(r'instructors', views.InstructorViewSet)
router.register(r'students', views.StudentViewSet)
router.register(r'courses', views.CourseViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls'))
]