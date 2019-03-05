from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from task1.router import ListReadOnlyRouter
from viewset_api import views

app_name = 'viewset'

router = DefaultRouter()
search_router = ListReadOnlyRouter()
search_router.register(r'users/search', views.SearchUserViewSet, base_name='search')
router.register(r'users', views.UserViewSet)
router.register(r'signup', views.SignupViewSet, base_name='signup')

urlpatterns = [
    url(r'login/$', views.LoginViewSet.as_view({'post': 'post'}), name='login'),
    url(r'logout/$', views.LogoutViewSet.as_view({'get': 'get'}), name='logout'),
    url('^', include(search_router.urls)),
    url('^', include(router.urls)),
]
