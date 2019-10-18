"""
Views Module.

This module generates views for home,
registration, viewing profile and
edit_profile.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import UserProfileForm, UpdateForm

# Create your views here.


def index(request):
    """View for Index Page."""
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = ''
    context = {'username': username}
    return render(request, 'index.html', context)


def register(request):
    """View for registration page."""
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserProfileForm()

    context = {'form': form}
    return render(request, 'users/register.html', context)


@login_required
def view_profile(request):
    """View for profile page."""
    return render(request, 'users/profile.html')


def edit_profile(request):
    """View for editing profile page."""
    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return render(request, 'users/profile.html')

    else:
        form = UpdateForm(instance=request.user)
        context = {'form': form}
        return render(request, 'users/edit_profile.html', context)
