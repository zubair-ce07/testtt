from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from viewset_api import views

app_name = 'viewset'
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'signup', views.SignupViewSet, base_name='signup')

urlpatterns = [
    url('^', include(router.urls)),
    url(r'login/$', views.LoginViewSet.as_view({'post': 'post'}), name='login'),
    url(r'logout/$', views.LogoutViewSet.as_view({'get': 'get'}), name='logout'),
]
