from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^api-token-auth/',obtain_jwt_token),
    url(r'^admin/', admin.site.urls),
    url(r'^music/', include('music.urls')),
    url(r'^', include('music.urls')),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


