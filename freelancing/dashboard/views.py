from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from accounts.forms import ProfileForm


@login_required()
def index(request):
    # redirect if no profile
    if not request.user.profile.description:
        return redirect('settings_profile')

    return render(request, 'dashboard/index.html')


@login_required()
def settings(request):
    return render(request, 'settings/settings.html')


@login_required()
def settings_profile(request):
    form = ProfileForm(instance=request.user.profile)
    context = {
        'form': form
    }

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()

            return redirect('settings')

    return render(request, 'profile/edit_profile.html', context)


@login_required()
def settings_change_password(request):

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            print("FORM IS VALID")
            user = form.save()
            update_session_auth_hash(request, user)  # Important!

            return redirect('settings')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})
