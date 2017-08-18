from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns

from classes import views

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^students/$', views.StudentList.as_view(), name='students-list'),
    url(r'^courses/$', views.CourseList.as_view(), name='courses-list'),
    url(r'^enrollments/$', views.EnrollmentList.as_view(), name='enrollments-list'),
    url(r'^instructors/$', views.InstructorList.as_view(), name='instructors-list'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = format_suffix_patterns(urlpatterns)
