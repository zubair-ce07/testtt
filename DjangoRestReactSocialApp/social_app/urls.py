from django.urls import path, include
from .views import *

from rest_framework.routers import DefaultRouter

post_router = DefaultRouter()
post_router.register('', PostViewSet)

comment_router = DefaultRouter()
comment_router.register('', CommentViewSet)


urlpatterns = [
    path('current_user', get_current_user),
    path('users', CreateUserView.as_view()),
    path('users/change', UpdateUserView.as_view()),

    path('posts/', include(post_router.urls)),

    path('comments/', include(comment_router.urls)),
]