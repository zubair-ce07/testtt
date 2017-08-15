"""djangorest URL Configuration

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
from django.conf.urls import url, include
from rest_framework.authtoken import views
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/user/', include('user.urls')),
    url(r'^api/comment/', include('comment.urls')),
    url(r'^api/blog/', include('blog.urls'))
]

urlpatterns += [
    url(r'^api-token-auth/', views.obtain_auth_token),
]

urlpatterns += [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
]
