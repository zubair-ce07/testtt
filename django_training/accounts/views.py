from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from accounts.forms import LoginForm, SignupForm
from blogs.models import Blog


def home(request):
    blogs = Blog.objects.all()
    return render(request, 'accounts/home.html', {'blogs': blogs})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=user_name, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse('<h1>Authentication Error {}: {} </h1>'.format(user_name, password))
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login'))
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
