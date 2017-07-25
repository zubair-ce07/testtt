from django.conf.urls import url
import views
app_name = "authentication"
urlpatterns = [
    url(r'^welcome/$|^$', views.WelcomeView.as_view(), name='welcome'),
    url(r'^login/$|^$', views.LoginView.as_view(), name='login'),
    url(r'^signup/$', views.SignupView.as_view(), name='signup'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
]
