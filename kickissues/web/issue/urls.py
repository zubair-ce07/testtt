from django.urls import path, re_path, include

from .views import (AssignView, CommentDeleteView, CommentEditView,
                    CreateIssueView, EditIssueView, IssueDetailView,
                    OpenAgainView, ResolveIssueView)

app_name = 'issue'

urlpatterns = [
    re_path('^api-auth/', include('rest_framework.urls')),
    path('create/', CreateIssueView.as_view(), name='create'),
    re_path(r'^(?P<pk>\d+)/$', IssueDetailView.as_view(), name="issuedetail"),
    re_path(r'^assign/(?P<id>\d+)/$', AssignView.as_view(), name="assign"),
    re_path(r'^edit/(?P<pk>\d+)/$', EditIssueView.as_view(), name="edit"),
    path('comment/edit/<int:id>/<int:pk>', CommentEditView.as_view(), name='comment_update'),
    path('comment/delete/<int:id>/<int:pk>', CommentDeleteView.as_view(), name='delete_comment'),
    re_path(r'^resolve/(?P<id>\d+)/$', ResolveIssueView.as_view(), name="resolve"),
    re_path(r'^open/(?P<id>\d+)/$', OpenAgainView.as_view(), name="open_again"),
    path('api/', include('web.issue.api.urls'))
]
