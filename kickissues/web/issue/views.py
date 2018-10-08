import datetime

from bootstrap_modal_forms.mixins import DeleteAjaxMixin, PassRequestMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import (
    CreateView, DeleteView, UpdateView, View
)

from .forms import CommentEditForm, CommentForm, IssueForm
from .models import Comment, Issue


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
        group = Group.objects.filter(user=request.user).first().name
        context = {}
        if group == 'Manager':
                context['manager'] = True
        if self.request.user == issue.created_by or self.request.user == issue.manage_by:
            context['form'] = self.form_class()
        context['comment_list'] = Comment.objects.filter(issue_id=pk).order_by('-timestamp')
        context['object'] = issue
        return render(request, 'issue/issue_detail.html', context)

    def post(self, request, pk):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            draft = form.save(commit=False)
            draft.comment_by = request.user
            issue = Issue.objects.get(id=pk)
            draft.issue_id = issue
            draft.save()
            return redirect('issue:issuedetail', pk=pk)
        return render(request, 'issue/issue_detail.html', {'form': form})


class AssignView(LoginRequiredMixin, View):
    login_url = 'account:login'

    def get(self, request, id):
        issue = Issue.objects.get(id=id)
        issue.manage_by = self.request.user
        issue.status = 'review'
        issue.assigned_date = datetime.datetime.now()
        issue.save()
        return redirect('issue:issuedetail', pk=id)


class EditIssueView(LoginRequiredMixin, UpdateView):
    login_url = 'account:login'
    model = Issue
    form_class = IssueForm
    template_name = 'issue/edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        issue = Issue.objects.get(id=self.object.pk)
        if issue.created_by == self.request.user:
            context["form"] = self.form_class(instance=issue)
        else:
            context["not_allowed"] = True
        return context

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


class ResolveIssueView(LoginRequiredMixin, View):
    login_url = 'account:login'

    def get(self, request, id):
        issue = Issue.objects.get(id=id)
        issue.status = 'resolved'
        issue.resolved_date = datetime.datetime.now()
        issue.save()
        return redirect('issue:issuedetail', pk=id)


class OpenAgainView(LoginRequiredMixin, View):
    login_url = 'account:login'

    def get(self, request, id):
        issue = Issue.objects.get(id=id)
        issue.status = 'review'
        issue.resolved_date = None
        issue.save()
        return redirect('issue:issuedetail', pk=id)
