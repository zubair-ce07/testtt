from django.conf.urls import url, include

from rest_framework import routers
from rest_framework.authtoken import views as authtoken_views

from . import views

router = routers.DefaultRouter()
router.register(r'assignments', views.AssignmentViewSet)
router.register(r'technologies', views.TechnologyViewSet)
router.register(r'trainers', views.TrainerViewSet)
router.register(r'trainees', views.TraineeViewSet)

app_name = "training_api"
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^assignments_assigned/$', views.AssignmentsAssigned.as_view(),
        name="assignments_assigned"),
    url(r'^trainer_assigned/$', views.TrainerAssigned.as_view(),
        name="trainer_assigned"),
    url(r'^trainees_assigned/$', views.TraineesAssigned.as_view(),
        name="trainees_assigned"),
    url(r'^search/$', views.Search.as_view(), name="search"),
    url(r'^profile/$', views.Profile.as_view(), name="profile"),
    url(r'^trainer_signup/$', views.TrainerSignUp.as_view(),
        name="trainer_signup"),
    url(r'^trainee_signup/$', views.TraineeSignUp.as_view(),
        name="trainee_signup"),
    url(r'^login/$', authtoken_views.obtain_auth_token),
]
