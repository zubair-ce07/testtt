from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^payment/', include('payment.urls')),
    url('^user/', include('users.urls')),
    url('^shopcity/', include('shopcity.urls')),
    url('^$', include('shopcity.urls')),
]
