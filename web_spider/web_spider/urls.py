"""web_spider URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from reviews.views import ReviewViewSet

urlpatterns = [
    url(r'reviews/$', ReviewViewSet.as_view({'post': 'create'})),
    url(r'reviews/(?P<movie_id>\d+)$', ReviewViewSet.as_view({'get': 'list'})),
    url(r'^admin/', admin.site.urls),
    url(r'^crawler/', include('url_crawler.urls')),
    url(r'^tz_detect/', include('tz_detect.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
