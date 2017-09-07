from django.conf.urls import url
from users import views


urlpatterns = [
    url(r'^get-token/', views.ObtainAuthToken.as_view())
]
