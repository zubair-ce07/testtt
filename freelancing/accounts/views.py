from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import Http404

from .forms import SignUpForm
from .models import User


def signin(request):
    """
        GET:
            Displays Login Form
        POST:
            Authenticate the user
            Redirects to Dashboard
    """
    # check if already login
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = AuthenticationForm(
            data=request.POST
        )
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/signin.html', {'form': form})


def signup(request):
    """
        GET:
            Displays Sign Up Form
        POST:
            Save the user
            Authenticate the user
            Redirects to Dashboard
    """
    # check if already login
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            # Saving user
            form.save()
            # Authenticating user to login
            username = request.POST.get("username")
            password = request.POST.get("password1")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')

    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})


def signout(request):
    """
        Logout the user and destroy the session
    """
    logout(request)
    return redirect('/')


def change_role(request):
    role = request.GET['role']

    if role is None:
        return redirect(request.url)

    if role == "seller":
        print("CHANGING ROLE TO SELLER")
        request.user.is_seller = True
        request.user.is_buyer = False
        request.user.save()

    if role == "buyer":
        print("CHANGING ROLE TO BUYER")
        request.user.is_seller = False
        request.user.is_buyer = True
        request.user.save()

    return redirect('/')
