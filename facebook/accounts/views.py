from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import FBUserCreationForm, FBUserChangeForm


def signup(request):
    if request.method == 'POST':
        form = FBUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = FBUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = FBUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = FBUserChangeForm(instance=request.user)
    return render(request, 'profile/info.html', {'form': form})
