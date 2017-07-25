from django.conf.urls import url

from users import views

app_name = 'users'

urlpatterns = [
    url(r'^details/$', views.DetailsView, name='details'),
    url(r'^edit/$', views.EditView, name='edit'),
    url(r'^signup/$', views.SignUpView, name='signup'),
    url(r'^login/$', views.LoginView, name='login'),
    url(r'^logout/$', views.LogoutView, name='logout'),
]
