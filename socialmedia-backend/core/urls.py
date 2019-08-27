from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path, include
from rest_framework import routers

from .views import (UserViewSet, PostViewSet, CommentViewSet, FollowingViewSet,
                    RegistrationAPIView, LoginAPIView, FeedAPIView)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'followings', FollowingViewSet)

app_name = 'core'

urlpatterns = [
    path('', include(router.urls)),
    path('feed/<int:user_id>', FeedAPIView.as_view()),
    path('register', RegistrationAPIView.as_view()),
    path('login', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
