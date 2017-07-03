from django.conf.urls import url

from main.views import SignUpView, HomeView, LoginView, logout_view, PostTweetView

app_name = 'main'
urlpatterns = [
    url(r'^home$', HomeView.as_view(), name='home'),
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^logout$', logout_view, name='logout'),
    url(r'^post_tweet$', PostTweetView.as_view(), name='post_tweet'),
]
