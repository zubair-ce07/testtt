from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from django.views.generic import TemplateView
from url_crawler.decorators import not_logged_in_required
from users import views

app_name = 'users'

urlpatterns = [
    url(r'^users/$', login_required(TemplateView.as_view(template_name='users/list_users.html')), name='index'),
    url(r'^login/$', not_logged_in_required(TemplateView.as_view(template_name='users/login.html')), name='login'),
    url(r'^create-user/$', login_required(TemplateView.as_view(template_name='users/create_user.html')), name='signup'),
    url(r'^users/(?P<pk>[0-9]+)/$',
        login_required(TemplateView.as_view(template_name='users/user_detail.html')), name='user_detail'),
    url(r'^logout/$', login_required(views.logout_user), name='logout'),
    url(r'^api/login/$', views.login_user)
]
