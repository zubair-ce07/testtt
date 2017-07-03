from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from main.models import Tweet
from main.forms import UserSignUpForm, LoginForm, TweetForm


# Create your views here.


def logout_view(request):
    logout(request)
    return redirect(reverse('main:home'))

class PostTweetView(View):
    def get(self,request):
        form = TweetForm()
        return render(request, 'main/post_tweet.html', {'form': form})

    def post(self,request):
        form = TweetForm(request.POST)
        if form.is_valid():
            Tweet.objects.create(user=request.user, **form.cleaned_data)
            return HttpResponseRedirect(reverse('main:home'))
        return render(request, 'main/post_tweet.html', {'form': form})



class HomeView(View):
    def get(self, request):
        context={'user': request.user}
        return render(request, 'main/home.html', context)


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'main/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('main:home'))
        return render(request, 'main/login.html', {'form': form})


class SignUpView(View):
    def get(self, request):
        form = UserSignUpForm()
        return render(request, 'main/singup.html', {'form': form})

    def post(self, request):
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            # redirect, or however you want to get to the main view
            return HttpResponseRedirect(reverse('main:home'))
        return render(request, 'main/singup.html', {'form': form})
