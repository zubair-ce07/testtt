"""
Views Module.

This module generates views for home,
registration, viewing profile and
edit_profile.
"""
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.views.generic import ListView
from django.shortcuts import render_to_response
from books import models as book_models
from users.models import UserProfile
from .forms import UserProfileForm, UpdateForm


class IndexView(View):
    """Class-based View for Index Page."""

    def get(self, request):
        """Get method for Index View."""
        username = ''
        context = {'username': username,
                   'is_librarian': UserProfile.objects.filter(
                       username=request.user.username,
                       groups__name='LIBRARIAN_GROUP_NAME').exists()}
        return render(request, 'index.html', context)

    def post(self, request):
        """Post method for Index View."""
        username = request.user.username
        context = {'username': username}

        return render(request, 'index.html', context)


class RegistrationView(View):
    """Class-based View for Registration Page."""
    def get(self, request):
        """Get method for Registration View."""
        registration_form = UserProfileForm()
        context = {'registration_form': registration_form}

        return render(request, 'users/register.html', context)

    def post(self, request):
        """Post method for Registration View."""
        registration_form = UserProfileForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            username = registration_form.cleaned_data.get('username')
            password = registration_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')

        context = {'registration_form': registration_form}
        return render(request, 'users/register.html', context)


class EditProfileView(View):
    """Class-based View for Edit Profile Page."""
    def get(self, request):
        """Get method for Edit Profile View."""
        update_form = UpdateForm(instance=request.user)
        context = {'update_form': update_form}
        return render(request, 'users/edit_profile.html', context)

    def post(self, request):
        """Post method for Edit Profile View."""
        update_form = UpdateForm(request.POST, instance=request.user)
        if update_form.is_valid():
            update_form.save()
            username = update_form.cleaned_data.get('username')
            password = update_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return render(request, 'users/profile.html')


class UserListView(ListView):
    """Class for viewing user list."""

    model = UserProfile
    template_name = 'users/user_detail.html'
    context_object_name = 'users'
    ordering = ['-username']


class ViewInfo(View):
    """To view user info."""

    def get(self, request, pk):
        """Get method for viewing user's info."""
        user = UserProfile.objects.get(id=pk)
        issued_books = book_models.IssueBook.objects.filter(user=user)
        context = {'user': user,
                   'issued_books': issued_books}
        return render_to_response('users/user_profile.html', context)
