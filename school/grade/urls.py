from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^grades/$',
        views.GradeList.as_view(),
        name='grade-list'
    ),
    url(
        r'^grades/(?P<grade_id>[0-9]+)/$',
        views.GradeDetail.as_view(),
        name='grade-detail'
    ),
    url(
        r'^grade_course/$',
        views.GradeCourseList.as_view(),
        name='gradecourse-list'
    ),
    url(
        r'^grade_course/(?P<gradecourse_id>[0-9]+)/$',
        views.GradeCourseDetail.as_view(),
        name='gradecourse-detail'
    ),

    url(
        r'^grade_teacher/$',
        views.GradeTeacherList.as_view(),
        name='gradeteacher-list'
    ),
    url(
        r'^grade_teacher/(?P<gradeteacher_id>[0-9]+)/$',
        views.GradeTeacherDetail.as_view(),
        name='gradeteacher-detail'
    ),
    
    url(
        r'^grade_student/$',
        views.GradeStudentList.as_view(),
        name='gradestudent-list'
    ),
    url(
        r'^grade_student/(?P<gradestudent_id>[0-9]+)/$',
        views.GradeStudentDetail.as_view(),
        name='gradestudent-detail'
    ),
]
