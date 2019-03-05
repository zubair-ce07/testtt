from django.urls import path, include

from web.issue.views import (AssignView, CommentDeleteView, CommentEditView,
                             CreateIssueView, EditIssueView, IssueDetailView,
                             OpenIssueAgainView, UpdateIssueStatusView)

app_name = 'issue'

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('create/', CreateIssueView.as_view(), name='create'),
    path('<int:pk>/', IssueDetailView.as_view(), name="issuedetail"),
    path('assign/', AssignView.as_view(), name="assign"),
    path('edit/<int:pk>/', EditIssueView.as_view(), name="edit"),
    path('comment/edit/<int:id>/<int:pk>', CommentEditView.as_view(), name='comment_update'),
    path('comment/delete/<int:id>/<int:pk>', CommentDeleteView.as_view(), name='delete_comment'),
    path('resolve/', UpdateIssueStatusView.as_view(), name="resolve"),
    path('open/', OpenIssueAgainView.as_view(), name="open_again"),
    path('api/', include('web.issue.api.urls'))
]
