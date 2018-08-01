from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('taskmanager/', include('taskmanager.urls')),
    path('admin/', admin.site.urls),
]
