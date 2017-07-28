from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from user_api import views

# urls for users api endpoints
router = DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('user_api.urls')),
    url(r'^', include(router.urls)),
]
