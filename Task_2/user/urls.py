from django.conf.urls import url
from django.views.generic import RedirectView

from user import views

app_name = 'user'

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='details', permanent=True)),
    url(r'^details/$', views.DetailsView, name='details'),
    url(r'^edit/$', views.EditView, name='edit'),
    url(r'^signup/$', views.SignUpView, name='signup'),
    url(r'^login/$', views.LoginView, name='login'),
    url(r'^logout/$', views.LogoutView, name='logout'),
]
