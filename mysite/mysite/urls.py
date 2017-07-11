
from django.conf.urls import include, url, static
from django.conf import settings
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', RedirectView.as_view(url='/store/brands/', permanent=False)),
    url(r'^store/', include('super_store.urls')),
    url(r'^user/', include('authentication.urls')),
] + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
