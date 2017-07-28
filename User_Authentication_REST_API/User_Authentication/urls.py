from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.documentation import include_docs_urls
from django.views.generic.base import RedirectView

admin.autodiscover()

urlpatterns = [
    url(r'^docs/', include_docs_urls(title='Training API')),
    url(r'^admin/', admin.site.urls),
    url(r'^users/', include("UserRegistration.urls")),
    url(r'^apicall/', include("rest_api.urls")),
    url(r'^$', RedirectView.as_view(pattern_name='users:login', permanent=False)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^cinescore/', include("cinescore_rest_api.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
