from django.conf.urls import include, url
from django.contrib import admin
from forms import views


handler404 = views.handler404
handler500 = views.handler500
handler400 = views.handler400

urlpatterns = [
    url(r'^', include('user.urls')),
    url(r'^user/', include('user.urls')),
    url(r'^articles/', include('articles.urls')),
    url(r'^admin/', admin.site.urls),
    url(
        r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')
    ),
]
