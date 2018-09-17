from django.views import generic
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse

from .forms import FeedbackForm
from .models import Feedback
from accounts.models import UserProfile


class PostFeedbackView(generic.FormView):
    template_name = 'feedback/give_feedback.html'
    form_class = FeedbackForm
    context_object_name = 'form'

    def form_valid(self, form):
        pair_user = get_object_or_404(UserProfile, pk=self.kwargs['pk'])
        new_feedback = Feedback()
        new_feedback.given_to_user = pair_user
        new_feedback.given_by_user = self.request.user.userprofile
        new_feedback.star_rating = form.cleaned_data.get('star_rating', 0)
        new_feedback.comments = form.cleaned_data.get('comments', '')
        new_feedback.save()
        return super(PostFeedbackView, self).form_valid(form)

    def get_success_url(self):
        pair_user = get_object_or_404(UserProfile, pk=self.kwargs['pk'])
        return reverse('accounts:home')
