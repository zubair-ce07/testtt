from django.conf.urls import url
from user_api import views


urlpatterns = [
    url(r'^get-token/', views.ObtainAuthToken.as_view())
]
