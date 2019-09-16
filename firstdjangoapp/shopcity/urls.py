from django.conf.urls import url

from .views import FileUpload, ViewResults, ProductView


urlpatterns = [
    url(r'^upload/', FileUpload.as_view(), name='upload_file'),
    url(r'^search/', ViewResults.as_view(), name='home_page'),
    url(r'^$', ViewResults.as_view(), name='home_page'),
    url(r'^(?P<product_id>[-\w]+)/', ProductView.as_view(), name='product_details'),
]
