from django.urls import path

from web.issue.api.views import (
    IssueListCreateAPIView,
    IssueRetriveUpdateDestroyAPIView,
    IssueStatusChangeAPIView,
    CommentListCreateAPIView,
    CommentRetriveUpdateDestoryAPIView
)

# app_name = 'api'

urlpatterns = [
    path('', IssueListCreateAPIView.as_view(), name="issue-list-create"),
    path('<int:pk>/', IssueRetriveUpdateDestroyAPIView.as_view(), name="issue-detail"),
    path('<int:pk>/status/', IssueStatusChangeAPIView.as_view(), name="issue-status"),
    path('<int:issueid>/comments/', CommentListCreateAPIView.as_view(), name="issue-comments"),
    path(
        '<int:issueid>/comments/<int:pk>/',
        CommentRetriveUpdateDestoryAPIView.as_view(),
        name="issue-comment-edit"
    ),

]
