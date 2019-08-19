from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import views as auth_views

from .models import User
from .forms import UserRegisterForm, UserUpdateForm, UserLoginForm
# Create your views here.


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f'Your account has been Created!')
#             return redirect('login')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'user_profile/register.html', {'form': form})


class Register(View):
    def post(self, request):
        form = UserRegisterForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been Created!')
            return redirect('login')
        return render(request, 'user_profile/register.html', {'form': form})

    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'user_profile/register.html', {'form': form})


class Profile(View):
    @method_decorator(login_required)
    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    @method_decorator(login_required)
    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        context = {
            'form': form
        }

        return render(request, 'user_profile/profile.html', context)


class LoginView(auth_views.LoginView):
    template_name = 'user_profile/login.html'
    form_class = UserLoginForm
