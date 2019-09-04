from django.urls import path, include
from rest_framework import routers

from core import views


router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'posts-media', views.PostMediaViewSet)

app_name = 'core'

urlpatterns = [
    path('posts/<int:pk>/comments/', views.PostCommentView.as_view()),
    path('posts/<int:pk>/media/', views.PostMediaView.as_view()),

    path('feed/<int:user_id>/', views.FeedView.as_view()),
]
