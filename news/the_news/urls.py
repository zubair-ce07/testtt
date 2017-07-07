__author__ = 'luqman'


from django.conf.urls import url, include
import views


app_name = "the_news"
urlpatterns = [
    url(r'^the_news/fetch/$', views.FetchView.as_view(), name='fetch_news'),
    url(r'^the_news/terminate/$', views.TerminateView.as_view(),
        name='terminate_fetch_news'),
    url(r'^the_news/$', views.TheNewsMainView.as_view(), name='main'),
]
