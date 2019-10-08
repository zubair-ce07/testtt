from django.shortcuts import render, redirect
from django.views import View
from .forms import FBUserCreationForm, FBUserChangeForm


class SignupView(View):
    @staticmethod
    def get(request):
        form = FBUserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})

    @staticmethod
    def post(request):
        form = FBUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'registration/signup.html', {'form': form})


class ProfileView(View):
    @staticmethod
    def get(request):
        form = FBUserChangeForm(instance=request.user)
        return render(request, 'profile/info.html', {'form': form})

    @staticmethod
    def post(request):
        form = FBUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        return render(request, 'profile/info.html', {'form': form})
