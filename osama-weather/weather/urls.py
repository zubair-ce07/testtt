from django.conf.urls import url, include

from rest_framework import routers

from weather import views

router = routers.DefaultRouter()
router.register(r'weather', views.WeatherViewSet)

urlpatterns = [
    url(r'^weather/summary/$', views.WeatherSummaryView.as_view()),
    url(r'^', include(router.urls)),
]
