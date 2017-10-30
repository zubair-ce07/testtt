import datetime

from django.contrib.auth import (
    authenticate, login as django_login,
    logout as django_logout
)
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from .forms import SigninForm, SignupForm, StatusForm
from .models import UserStatus, UserFollowers


class SignIn(View):
    template_name = 'myfacebook/signin.html'

    def get(self, request):
        form = SigninForm(None)
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        message = ''
        form = SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                django_login(request, user)
                return redirect('myfacebook:profile')
            else:
                message += 'SignIn failed'
        context = {
            'error': message
        }
        return render(request, self.template_name, context)


class Signup(View):
    template_name = 'myfacebook/signup.html'

    def get(self, request):
        context = {
            'form': SignupForm(None)
        }
        return render(request, self.template_name, context)

    def post(self, request):
        message = ''
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                django_login(request, user)
                return redirect('myfacebook:profile')
            else:
                message += '\nSignIn failed'
        else:
            message += '\nForm not valid'
        context = {
            'form': form,
            'error': message
        }
        return render(request, self.template_name, context)


class Logout(View):
    def get(self, request):
        django_logout(request)
        return redirect('myfacebook:signin')


class Profile(View):
    template_name = 'myfacebook/profile.html'

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            statuses = UserStatus.objects.filter(status_author=user)
            context = {
                'user': user,
                'statuses': statuses,
                'form': StatusForm(None)
            }
            return render(request, self.template_name, context)

        return redirect('myfacebook:signin')

    def post(self, request):
        user = request.user
        form = StatusForm(request.POST)
        if form.is_valid():
            status = UserStatus(status_text=form.cleaned_data['status'],
                                status_author=user,
                                pub_date=datetime.datetime.now())
            status.save()
            return redirect('myfacebook:profile')

        context = {
            'form': StatusForm(None),
            'user': user,
            'message': 'status is invalid',
        }
        return render(request, self.template_name, context)


class FindPeople(View):
    template_name = 'myfacebook/find.html'

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            users = User.objects.exclude(id=user.id)
            context = {
                'users': users
            }
            return render(request, self.template_name, context)

        return redirect('myfacebook:signin')


class UserDetails(View):
    template_name = 'myfacebook/detail.html'

    def get(self, request, user_id):
        current_user = request.user
        if current_user.is_authenticated:
            user = User.objects.get(id=user_id)
            statuses = UserStatus.objects.filter(status_author=user)
            is_following = UserFollowers.objects.filter(followee=user, follower=current_user).count()
            context = {
                'user': user,
                'statuses': statuses,
                'is_following': is_following
            }
            return render(request, self.template_name, context)

        return redirect('myfacebook:signin')


def follow(request, user_id):
    current_user = request.user
    if current_user.is_authenticated:
        user = User.objects.get(id=user_id)
        user_follow = UserFollowers(followee=user, follower=current_user)
        user_follow.save()
        return redirect('myfacebook:detail', user_id)

    return redirect('myfacebook:signin')


class HomePage(View):
    template_name = 'myfacebook/home.html'

    def get(self, request):
        current_user = request.user
        if current_user.is_authenticated:
            followings = UserFollowers.objects.filter(follower=current_user)
            statuses = []
            for following in followings:
                statuses += UserStatus.objects.filter(status_author=following.followee)

            context = {
                'statuses': statuses
            }
            return render(request, self.template_name, context)

        return redirect('myfacebook:signin')
