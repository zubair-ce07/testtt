from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from learnerapp import views


router = DefaultRouter()
router.register(r'instructors', views.InstructorViewSet)
router.register(r'students', views.StudentViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'enrollments', views.EnrollmentView, base_name='learnerapp')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^unenroll/(?P<pk>\d+)/', views.UnenrollView.as_view(), name='unenroll'),
    url(r'^api-auth/', include('rest_framework.urls'))
]