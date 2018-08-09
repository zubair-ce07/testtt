from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('taskmanager/', include('taskmanager.urls'), name='taskmanager'),
    path('taskmanager/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Task Manager Admin"
admin.site.site_title = "Task Manager Admin Portal"