from django.conf.urls import url

from .views import DetailsView, EditView

app_name = 'registration'

urlpatterns = [
    url(r'^details/$', DetailsView, name='details'),
    url(r'^edit/$', EditView , name='edit'),
]
