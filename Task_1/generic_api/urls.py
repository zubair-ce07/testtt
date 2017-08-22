from django.conf.urls import url

from generic_api import views

app_name = 'generic'

urlpatterns = [
    url(r'users/$', views.UserListView.as_view(), name='list'),
    url(r'users/(?P<pk>[0-9]+)/$', views.UserDetailView.as_view(), name='details'),
    url(r'login/$', views.LoginView.as_view(), name='login'),
    url(r'signup/$', views.SignupView.as_view(), name='signup'),
    url(r'logout/$', views.LogoutView.as_view(), name='logout'),
]
