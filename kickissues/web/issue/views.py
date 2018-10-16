from bootstrap_modal_forms.mixins import DeleteAjaxMixin, PassRequestMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import (
    CreateView, DeleteView, UpdateView, View
)

from web.account.mixins import IssueOwnerPermissionMixin
from web.account.utils import is_manager
from web.issue.forms import CommentEditForm, CommentForm, IssueForm
from web.issue.models import Comment, Issue, StatusChoices


class CreateIssueView(LoginRequiredMixin, CreateView):
    login_url = 'account:login'
    redirect_field_name = 'issue:create'
    template_name = 'issue/create.html'
    form_class = IssueForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('account:dashboard')


class IssueDetailView(LoginRequiredMixin, View):
    login_url = 'account:login'
    form_class = CommentForm

    def get(self, request, pk):
        issue = Issue.objects.get(id=pk)
        context = {'manager': is_manager(request.user)}
        if self.request.user == issue.created_by or self.request.user == issue.manage_by:
            context['form'] = self.form_class()
        context['comment_list'] = Comment.objects.filter(issue_id=pk).order_by('-timestamp')
        context['object'] = issue
        return render(request, 'issue/issue_detail.html', context)

    def post(self, request, pk):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            draft_issue = form.save(commit=False)
            draft_issue.comment_by = request.user
            issue = Issue.objects.get(id=pk)
            draft_issue.issue = issue
            draft_issue.save()
            return redirect('issue:issuedetail', pk=pk)

        return render(request, 'issue/issue_detail.html', {'form': form})


class AssignView(LoginRequiredMixin, View):
    login_url = 'account:login'

    def post(self, request):
        if is_manager(request.user):
            issue_id = request.POST.get("id")
            issue = Issue.objects.get(id=issue_id)
            issue.manage_by = self.request.user
            issue.status = StatusChoices.REVIEW
            issue.assigned_at = timezone.datetime.now()
            issue.save()
        else:
            raise PermissionDenied("You don't have access to this page")
        return redirect('issue:issuedetail', pk=issue_id)


class EditIssueView(LoginRequiredMixin, IssueOwnerPermissionMixin, UpdateView):
    login_url = 'account:login'
    model = Issue
    form_class = IssueForm
    template_name = 'issue/edit.html'

    def get_success_url(self):
        return reverse('issue:issuedetail', args=[self.object.pk])


class CommentEditView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    template_name = "issue/comment_edit.html"
    form_class = CommentEditForm
    success_message = 'Success: Comment Updated.'
    model = Comment

    def get_success_url(self):
        return reverse('issue:issuedetail', args=[self.kwargs["id"]])


class CommentDeleteView(DeleteAjaxMixin, DeleteView):
    model = Comment
    template_name = 'issue/delete_comment.html'
    success_message = 'Success: Comment was deleted.'

    def get_success_url(self):
        return reverse('issue:issuedetail', args=[self.kwargs["id"]])


class UpdateIssueStatusView(LoginRequiredMixin, View):
    login_url = 'account:login'

    def post(self, request):
        if is_manager(request.user):
            issue_id = request.POST.get("id")
            issue = Issue.objects.get(id=issue_id)
            if issue:
                issue.status = StatusChoices.RESOLVED
                issue.resolved_at = timezone.datetime.now()
                issue.save()
        else:
            raise PermissionDenied("You don't have access to this page")
        return redirect('issue:issuedetail', pk=issue_id)


class OpenIssueAgainView(LoginRequiredMixin, IssueOwnerPermissionMixin, View):
    login_url = 'account:login'

    def post(self, request):
        issue_id = request.POST.get("id")
        issue = Issue.objects.get(id=issue_id)
        if issue:
            issue.status = StatusChoices.REVIEW
            issue.resolved_at = None
            issue.save()
        return redirect('issue:issuedetail', pk=issue_id)
