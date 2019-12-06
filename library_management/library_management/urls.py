from django.contrib import admin
from django.urls import include, path


def create_api_path(app_name):
    return path('api/', include(f"{app_name}.urls"))


library_apps = ['authors', 'books', 'categories', 'users',  'publishers', ]
library_urls = [create_api_path(appname) for appname in library_apps]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
] + library_urls
