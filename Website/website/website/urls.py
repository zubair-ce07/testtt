from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^users/', include('users.urls'), name='users'),
    url(r'^$', RedirectView.as_view(pattern_name='users:profile', permanent=False)),
]
