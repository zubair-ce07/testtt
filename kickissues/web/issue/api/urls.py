from django.urls import path, re_path

from .views import (
    IssueListCreateView,
    IssueRetriveUpdateDestroyView,
    IssueStatusChangeView,
    CommentListView,
    CommentRetriveUpdateDestoryView
)

# app_name = 'api'

urlpatterns = [
    path('', IssueListCreateView.as_view(), name="issue-list-create"),
    re_path('^(?P<pk>\d+)/$', IssueRetriveUpdateDestroyView.as_view(), name="issue-detail"),
    re_path('^(?P<pk>\d+)/status/$', IssueStatusChangeView.as_view(), name="issue-status"),
    re_path('^(?P<issueid>\d+)/comments/$', CommentListView.as_view(), name="issue-comments"),
    re_path(
        '^(?P<issueid>\d+)/comments/(?P<pk>\d+)$',
        CommentRetriveUpdateDestoryView.as_view(),
        name="issue-comment-edit"
    ),

]
