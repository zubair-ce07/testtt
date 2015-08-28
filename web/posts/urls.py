from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from web.posts.views.all_posts_viewset import AllPostsViewSet
from web.posts.views.my_posts_viewset import MyPostsViewSet
from web.posts.views.requests_list import RequestListViewSet
from web.posts.views.requests_viewset import RequestViewSet

router = DefaultRouter()
router.register(r'all', AllPostsViewSet)
router.register(r'my-posts', MyPostsViewSet)
router.register(r'requests', RequestViewSet)
router.register(r'requestslist', RequestListViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
]