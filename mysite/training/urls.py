from django.conf.urls import url

from . import views

app_name = "training"
urlpatterns = [
    url(r'^trainee/(?P<trainee_id>[0-9]+)/$',
        views.TraineeDetails.as_view(), name="trainee_details"),
    url(r'^trainer/(?P<trainer_id>[0-9]+)/$',
        views.TrainerDetails.as_view(), name="trainer_details"),
    url(r'^assignment/(?P<assignment_id>[0-9]+)/$',
        views.AssignmentDetails.as_view(), name="assignment_details"),
    url(r'^technology/(?P<technology_id>[0-9]+)/$',
        views.TechnologyDetails.as_view(), name="technology_details"),
    url(r'^search/$', views.Search.as_view(), name="search"),
    url(r'^trainer_signup/$',
        views.TrainerSignUp.as_view(), name="trainer_signup"),
    # url(r'^trainee_signup/$',
    #     views.TraineeSignUp.as_view(), name="trainee_signup"),
    url(r'^training_index/$',
        views.TrainingIndex.as_view(), name="training_index"),
    url(r'^signup/$', views.Signup.as_view(), name="signup"),
    url(r'^logout/$', views.Logout.as_view(), name="logout"),
    url(r'^login/$|^$', views.Login.as_view(), name="login"),
]
