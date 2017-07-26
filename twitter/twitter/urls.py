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
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from twitter import views, settings

urlpatterns = [
                  url(r'^admin/', admin.site.urls),

                  url(r'^$', views.HomeView.as_view(), name='home'),
                  url(r'^login/$', auth_views.login, {'template_name': 'twitter/login.html'},
                      name='login'),
                  url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
                  url(r'^logout/$', auth_views.logout, name='logout'),
                  url(r'^tweet/$', login_required()(views.TweetView.as_view()), name='tweet'),
                  url(r'^profiles/(?P<username>[a-zA-Z0-9@.+-_]+)/$',
                      login_required()(views.ProfileView.as_view()), name='profile'),

                  url(r'^follow', require_POST(views.FollowView.as_view()), name='follow'),
                  url(r'^news/$', login_required()(views.NewsView.as_view()), name='news'),
                  url(r'^news/(?P<pk>[\d]+)$', login_required()(views.NewsDetailedView.as_view()),
                      name='news_detailed'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
