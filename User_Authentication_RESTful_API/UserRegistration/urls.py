from django.conf.urls import url
from rest_framework.authtoken import views as v
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = "users"

urlpatterns = [

    url(r'^home/$', views.UsersTaskList.as_view(), name='home'),
    url(r'^user_tasks/(?P<pk>[0-9]+)/$', views.UserTaskDetails.as_view()),
    url(r'^user/$', views.CustomUserList.as_view()),
    url(r'^get_current_user/', views.GetCurrentUserDetails.as_view()),
    url(r'^user_profile_options/$', views.GetUpdateDeleteUserAPIView.as_view()),
    url(r'^login/$', v.obtain_auth_token),
]

urlpatterns = format_suffix_patterns(urlpatterns)