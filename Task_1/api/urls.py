from django.conf.urls import url

from api import views

app_name = 'api'

urlpatterns = [
    url(r'^list_api/$', views.UserListAPI.as_view(), name='list-api'),
    url(r'^details_api/$', views.UserDetailAPI.as_view(), name='details-api'),
    url(r'^details/$', views.UserProfileDetails.as_view(), name='details'),
    url(r'^edit/$', views.UserProfileEdit.as_view(), name='edit'),
    url(r'^signup/$', views.SignupView.as_view(), name='signup'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^$', views.api_root),
]
