from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from viewset_api import views

app_name = 'viewset'
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'signup', views.Signup, base_name='signup')

urlpatterns = [
    url('^', include(router.urls)),
    url(r'login/$', views.Login.as_view({'post': 'post'}), name='login'),
    url(r'logout/$', views.Logout.as_view({'get': 'get'}), name='logout'),
]
