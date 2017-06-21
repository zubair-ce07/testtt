from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.views.generic.edit import UpdateView
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm
from django.core.urlresolvers import reverse_lazy


class UserRegisterFormView (View):
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})
        pass

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return redirect('users:login')
        return render(request, self.template_name, {'form': form})


class UserLoginFormView (View):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('users:profile')
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})


class UserUpdate(UpdateView):
    form_class = UserUpdateForm
    template_name = 'users/edit.html'
    success_url = reverse_lazy('users:profile')
    
    def get_object(self, queryset=None):
        return self.request.user


def get_user_profile(request):
    return render(request, 'users/view.html', {"user": request.user})


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    return render(request, 'users/profile.html')


def logout_view(request):
    logout(request)
    return redirect('users:login')
