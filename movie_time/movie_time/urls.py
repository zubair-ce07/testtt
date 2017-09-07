from movies.views import index
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from users import views


router = DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^$', index),
    url(r'^', include('users.urls')),
    url(r'^', include(router.urls)),
]
