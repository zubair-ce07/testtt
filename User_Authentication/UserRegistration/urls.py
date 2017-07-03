from django.conf.urls import url
from . import views

app_name = "users"

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url(r'^login$', views.LoginView.as_view(), name='login'),
    url(r'^signup$', views.SignUpView.as_view(), name='signup'),
    url(r'^profiles$', views.ProfileView.as_view(), name='profile'),
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),
]