from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse

from registration.models import CustomUser
from .forms import UserLoginForm


def SignUpView(request):
    if request.method == 'GET':
        form = UserCreationForm()
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password1']
            raw_password = make_password(raw_password)
            user = CustomUser(username=username, password=raw_password)
            user.save()
            request.session['userid'] = str(user.id)
            login(request, user)
            return HttpResponseRedirect(redirect_to=reverse('registration:details'))
    return render(request, 'accounts/signup.html', {'form': form})


def LoginView(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to=reverse('registration:details'))
    if request.method == 'GET':
        form = UserLoginForm()
    else:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print('user: ', password)
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                if user.is_active:
                    request.session['userid'] = str(user.id)
                    login(request, user)
                    return HttpResponseRedirect(redirect_to=reverse('registration:details'))
    return render(request, 'accounts/login.html', {'form': form})


def LogoutView(request):
    logout(request)
    return HttpResponseRedirect(redirect_to=reverse('login'))
