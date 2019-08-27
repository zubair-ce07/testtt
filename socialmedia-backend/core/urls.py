from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path, include
from rest_framework import routers

from .views import (UserViewSet, PostViewSet, CommentViewSet, FollowingViewSet,
                    RegistrationAPIView)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'followings', FollowingViewSet)

app_name = 'core'

urlpatterns = [
    path('', include(router.urls)),
    path('register', RegistrationAPIView.as_view()),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
