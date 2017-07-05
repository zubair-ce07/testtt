from django.conf.urls import url

from . import views

app_name = 'users'
urlpatterns = [
    url(r'^register/$', views.UserRegisterFormView.as_view(), name='sign-up'),
    url(r'^login/$', views.UserLoginFormView.as_view(), name='login'),
    url(r'^profile/$', views.ProfilePage.as_view(), name='profile'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^edit/$', views.UserUpdate.as_view(), name='edit'),
    url(r'^view/$', views.ProfileView.as_view(), name='view'),
]
