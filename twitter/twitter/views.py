from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.functional import cached_property
from django.views import View
from django.views.generic import FormView, TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from twitter import forms
from twitter.models import Tweet, User


class TweetView(LoginRequiredMixin, FormView):
    template_name = 'twitter/tweet.html'
    form_class = forms.TweetForm

    def form_valid(self, form):
        Tweet.objects.create(user=self.request.user, **form.cleaned_data)
        return HttpResponseRedirect(reverse('home'))

    def form_invalid(self, form):
        return render(self.request, 'twitter/tweet.html', {'form': form})


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'twitter/profile.html'

    @cached_property
    def tweets(self):
        tweet_set = Tweet.objects.filler_by_username(username=self.kwargs['username'])
        return tweet_set

    @cached_property
    def profile_user(self):
        profile_user = User.objects.get_by_username(self.kwargs['username'])
        return profile_user

    @cached_property
    def form(self):
        form = forms.FollowForm(initial={'follower_username': self.profile_user.username})
        return form


class HomeView(ListView):
    template_name = 'twitter/home.html'
    model = Tweet
    context_object_name = 'tweets'


class FollowView(View):
    def post(self, request):
        profile_username = request.POST['follower_username']
        profile_user = get_object_or_404(User, username__iexact=profile_username)
        request.user.followers.add(profile_user)
        return redirect(reverse('profile', kwargs={'username': profile_username}))


class SignUpView(FormView):
    form_class = forms.UserSignUpForm
    template_name = 'twitter/singup.html'

    def form_valid(self, form):
        new_user = form.save()
        login(self.request, new_user)
        return HttpResponseRedirect(reverse('home'))
