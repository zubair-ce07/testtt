from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^crawler/', include('url_crawler.urls')),
    url(r'^tz_detect/', include('tz_detect.urls')),
    url(r'^reporting/', include('malfunction_reporting.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
