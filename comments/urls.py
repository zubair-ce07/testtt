from django.urls import path

from comments.views import CommentsList, FollowsList, CreateComment, CreateFollow, CommentDetail, FollowDetail

urlpatterns = [
    path('comments/', CommentsList.as_view(), name='comment-list'),
    path('follows/', FollowsList.as_view(), name='follow-list'),
    path('comments/<int:pk>', CommentDetail.as_view(), name='comment-detail'),
    path('follows/<int:pk>', FollowDetail.as_view(), name='follow-detail'),
    path('comments/add', CreateComment.as_view(), name='add-comment'),
    path('follows/add', CreateFollow.as_view(), name='add-follow'),
]
