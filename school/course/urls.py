from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^courses/$',
        views.CourseList.as_view(),
        name='course-list'
    ),
    url(
        r'^courses/(?P<course_id>[0-9]+)/$',
        views.CourseDetail.as_view(),
        name='course-detail'
    ),
]
