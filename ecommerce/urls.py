""" Main  application urls what action to perform. """

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from users.views import ProductsList

urlpatterns = [
    path('', ProductsList.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('shop/', include('users.urls')),
    path('shop/', include('django.contrib.auth.urls')),
    path('manager/', include('manager.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
