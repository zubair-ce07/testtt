from django.shortcuts import render, redirect
from django.contrib import messages
from . import forms as user_forms
from django.views import generic
from django.contrib.auth.decorators import login_required
from .constants import UserConstants
from django.contrib.auth import authenticate, login


class RegisterUser(generic.CreateView):
    form_class = user_forms.UserRegistrationForm
    success_url = '/home'

    def form_valid(self, form):
        messages.success(self.request, UserConstants.ACCOUNT_CREATED_MESSAGE)
        return super(RegisterUser, self).form_valid(form)

    def get_success_url(self):
        user = authenticate(username=self.request.POST['username'], password=self.request.POST['password1'])
        login(self.request, user)
        return self.success_url


@login_required
def profile(request):
    if request.method == 'POST':
        form_user = user_forms.UserUpdateForm(request.POST, instance=request.user)
        form_profile = user_forms.ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form_user.is_valid() and form_profile.is_valid():
            form_user.save()
            form_profile.save()
            messages.success(request, UserConstants.PROFILE_UPDATE_MESSAGE)
            return redirect('profile')
    else:
        form_user = user_forms.UserUpdateForm(instance=request.user)
        form_profile = user_forms.ProfileUpdateForm(instance=request.user.profile)

    return render(request=request, template_name='user/profile.html',
                  context={'form_user': form_user, 'form_profile': form_profile})

