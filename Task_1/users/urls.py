from django.conf.urls import url

from users import views

app_name = 'users'

urlpatterns = [
    url(r'^details/$', views.UserDetailView, name='details'),
    url(r'^edit/$', views.UserEditView, name='edit'),
    url(r'^list/$', views.UserListView.as_view(), name='list'),
    url(r'^signup/$', views.SignUpView, name='signup'),
    url(r'^login/$', views.LoginView, name='login'),
    url(r'^logout/$', views.LogoutView, name='logout'),
]

