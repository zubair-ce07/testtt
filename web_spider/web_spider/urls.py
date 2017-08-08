from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from users import views


# urls for users api endpoints
router = DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^tz_detect/', include('tz_detect.urls')),
    url(r'^crawler/', include('url_crawler.urls')),
    url(r'^reporting/', include('malfunction_reporting.urls')),
    url(r'^', include(router.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
