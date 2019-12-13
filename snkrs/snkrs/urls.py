from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from snkr.views import search, show_data, upload_file

urlpatterns = [
    path('upload-csv/', upload_file, name="upload_file"),
    path('upload-csv/show_data', show_data, name="show_data"),
    path('upload-csv/search', search, name="search"),
    url(r'^admin/', admin.site.urls),
]
