from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from web.account.utils import is_manager
from web.issue.models import Issue, Comment
from .paginations import CustomPageNumberPagination
from .permissions import IsCommentedAndCanChange, IsOwnerOrManager, IsOwner
from .serializers import IssueCreateUpdateSerializer, IssueStatusChangeSerializer, CommentSerializer


class IssueListCreateView(ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueCreateUpdateSerializer
    permission_classes = ([IsAuthenticated, IsOwnerOrManager])
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description', 'priority']
    pagination_class = CustomPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        if is_manager(self.request.user):
            query_set = Issue.objects.filter(manage_by=self.request.user)
        else:
            query_set = Issue.objects.filter(created_by=self.request.user)

        return query_set


class IssueRetriveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueCreateUpdateSerializer
    permission_classes = ([IsAuthenticated, IsOwnerOrManager, IsOwner])


class IssueStatusChangeView(RetrieveUpdateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueStatusChangeSerializer
    permission_classes = ([IsAuthenticated, IsOwnerOrManager])


class CommentRetriveUpdateDestoryView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentedAndCanChange]


class CommentListView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        issueid = self.kwargs['issueid']
        issue = Issue.objects.filter(id=issueid, created_by=self.request.user).exists()
        if not issue:
            raise PermissionDenied("You are not allowed to see comments from this issue")
        return Comment.objects.filter(issue_id=issueid)

    def perform_create(self, serializer):
        issue_id = self.kwargs["issueid"]
        issue = Issue.objects.get(id=issue_id)
        serializer.save(issue_id=issue, comment_by=self.request.user)

