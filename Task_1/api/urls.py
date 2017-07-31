from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token

from api import views

app_name = 'api'

urlpatterns = [
    url(r'^list/$', views.UserList.as_view(), name='list'),
    url(r'^detail/$', views.UserDetail.as_view(), name='detail'),
    url(r'^details/$', views.UserProfileDetails.as_view(), name='details'),
    url(r'^edit/$', views.UserProfileEdit.as_view(), name='edit'),
    url(r'^signup/$', views.SignupView.as_view(), name='signup'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    # url(r'^login/', obtain_jwt_token),
    url(r'^$', views.api_root),
]
