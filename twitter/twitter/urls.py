"""twitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from twitter import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^tweet/$', login_required()(views.TweetView.as_view()), name='tweet'),
    url(r'^profiles/(?P<username>[\w]+)/$',
        login_required()(views.ProfileView.as_view()), name='profile'),
    url(r'^follow',require_POST(views.FollowView.as_view()), name='follow')
]
