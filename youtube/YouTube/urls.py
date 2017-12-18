from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from YouTube import views

# router = DefaultRouter()
# router.register(r'videos', views.VideoViewSet)
# router.register(r'users', views.UserViewSet)
urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^users/$', views.UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(),
        name='user-detail'),
    url(r'^videos/$', views.VideoList.as_view(), name='video-list'),
    url(r'^videos/(?P<pk>[0-9]+)/$', views.VideoDetail.as_view(),
        name='video-detail'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += [
    # url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework'))
]
