from django.conf.urls import url

from accounts import views

urlpatterns = [
    url(r'^accounts/signup', views.signup, name='signup'),
]

urlpatterns += [
    url(r'profile/$', views.profile, name='profile'),
    url(r'profile/update', views.update_profile, name='profile_update')
]
