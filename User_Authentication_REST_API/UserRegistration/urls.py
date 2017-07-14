from . import views
from .views import CustomUserList
from django.conf.urls import url, include
from rest_framework.authtoken import views as v
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user', CustomUserList, base_name='sample')

app_name = "users"

urlpatterns = [

    url(r'^tasks/$', views.UsersTaskList.as_view(), name='home'),
    url(r'^user_tasks/(?P<pk>[0-9]+)/$', views.UserTaskDetails.as_view()),
    url(r'^get_current_user/', views.GetCurrentUserDetails.as_view()),
    url(r'^user_profile_options/$', views.GetUpdateDeleteUserAPIView.as_view()),
    url(r'^login/$', v.obtain_auth_token),
    url(r'^', include(router.urls)),
]

