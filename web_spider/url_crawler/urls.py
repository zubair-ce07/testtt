from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from url_crawler import views


urlpatterns = [
    url(r'^$', login_required(views.Index.as_view()), name='index'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^signup/$', views.SignUp.as_view(), name='signup'),
    url(r'^logout/$', views.logout_user, name='logout')
]
