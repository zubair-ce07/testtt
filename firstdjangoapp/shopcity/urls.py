from django.conf.urls import url

from .views import FileUpload, ViewResults


urlpatterns = [
    url(r'^upload/', FileUpload.as_view(), name='upload_file'),
    url(r'^search/', ViewResults.as_view(), name='product_search'),
]
