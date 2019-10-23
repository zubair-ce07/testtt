from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from users.views import ShowProducts
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', ShowProducts.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
