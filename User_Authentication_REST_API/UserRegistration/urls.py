from . import views
from .views import CustomUserList
from django.conf.urls import url, include
from rest_framework.authtoken import views as v
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user', CustomUserList, base_name='list-detail')

app_name = "users"

urlpatterns = [

    url(r'^tasks/$', views.UsersTaskListCreateView.as_view(), name='home'),
    url(r'^task_details/(?P<pk>[0-9]+)/$', views.UserTaskDetails.as_view()),
    url(r'^user_profile_options/$', views.GetUpdateDeleteUserAPIView.as_view()),
    url(r'^login/$', v.obtain_auth_token),
    url(r'^', include(router.urls)),
]

