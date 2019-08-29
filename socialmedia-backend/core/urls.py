from rest_framework_simplejwt import views as jwt_views
from django.urls import path, include
from rest_framework import routers

from core import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'followings', views.FollowingViewSet)

app_name = 'core'

urlpatterns = [
    path('posts/<int:pk>/comments/', views.PostCommentView.as_view()),
    path('users/<int:pk>/posts/', views.UserPostView.as_view()),
    path('users/<int:pk>/followings/', views.UserFollowingView.as_view()),

    path('feed/<int:user_id>/', views.FeedView.as_view()),

    path('register', views.RegistrationView.as_view()),
    path('login', views.LoginView.as_view()),
    path('login/refresh', jwt_views.TokenRefreshView.as_view()),

    path('', include(router.urls)),
]
