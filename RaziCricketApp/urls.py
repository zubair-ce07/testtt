"""RaziCricketApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from articles.views import ArticleViewSet


# Routers provide an easy way of automatically determining the URL conf.
from users.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'articles', ArticleViewSet)

urlpatterns = [
    path('articles/', include('articles.urls')),
    path('comments/', include('comments.urls')),
    path('teams/', include('teams.urls')),
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),

    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
