from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('taskmanager/', include('taskmanager.urls'), name='taskmanager'),
    path('taskmanager/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]
