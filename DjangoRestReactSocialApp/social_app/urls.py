from django.urls import path
from .views import *

urlpatterns = [
    path('current_user', get_current_user),
    path('users', CreateUserView.as_view()),

    path('posts', PostView.as_view()),
    path('posts/<pk>', PostView.as_view()),

    path('comments', CommentView.as_view()),
    path('comments/<pk>', CommentView.as_view()),
]