from django.conf.urls import url
from rest_framework.authtoken import views as authtoken_views

from . import views

app_name = 'myfacebook'

urlpatterns = [
    url(r'^$', views.SignIn.as_view(), name='signin'),
    url(r'^home/$', views.HomePage.as_view(), name='home'),
    url(r'^find/$', views.FindPeople.as_view(), name='find'),
    url(r'^signup/$', views.Signup.as_view(), name='signup'),
    url(r'^logout/$', views.Logout.as_view(), name='logout'),
    url(r'^profile/$', views.Profile.as_view(), name='profile'),
    url(r'^news/$', views.NewsFeed.as_view(), name='latest'),
    url(r'^follow/(?P<user_id>[0-9]+)/$', views.follow, name='follow'),
    url(r'^news/(?P<news_id>[0-9]+)/$', views.NewsDetail.as_view(), name='news'),
    url(r'^profile/(?P<user_id>[0-9]+)/$', views.UserDetails.as_view(), name='detail'),
    url(r'^newsapi/$', views.NewsAPI.as_view()),
    url(r'^newsapi/(?P<pk>[0-9]+)/$', views.NewsAPI.as_view()),
    url(r'^funcnews/(?P<pk>[0-9]+)/$', views.user_news_view),
    url(r'^login/$', authtoken_views.obtain_auth_token),
]