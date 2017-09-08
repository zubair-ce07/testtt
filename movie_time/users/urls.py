from django.conf.urls import url
from users import views


urlpatterns = [
    url(r'^get-token/', views.obtain_auth_token)
]
