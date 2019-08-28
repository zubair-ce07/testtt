from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^settings$', views.settings, name="settings"),
    url(r'^settings/profile$', views.settings_profile, name="settings_profile"),
    url(r'^settings/accounts/change_password$',
        views.settings_change_password, name="settings_change_password")
]
