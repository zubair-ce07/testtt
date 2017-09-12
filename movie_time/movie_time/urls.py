from django.conf import settings
from django.conf.urls import url, include, static
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from users import views


router = DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('movies.urls')),
    url(r'^', include('users.urls')),
    url(r'^', include('watchlists.urls')),
    url(r'^', include(router.urls)),
]

urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
