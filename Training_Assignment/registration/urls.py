from django.conf.urls import url

from registration import views

app_name = 'registration'

urlpatterns = [
    url(r'^details/$', views.DetailsView, name='details'),
    url(r'^edit/$', views.EditView, name='edit'),
    url(r'^test/$', views.TestView, name='test')
]
