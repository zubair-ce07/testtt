# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views import View
from django.urls import reverse, reverse_lazy
from messages import Message
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from forms import LoginForm, SignupForm


class LoginView(View):
    template_name = 'authentication/login.html'
    form_class = LoginForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('authentication:welcome'))

        form = self.form_class(
            None, initial={'username': request.GET.get('username', '')})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('authentication:welcome'))

        form = self.form_class(request.POST)
        message = ''
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(self.request, user)
                    # Redirect to a success page.
                    return redirect(reverse('authentication:welcome'))
                else:
                    message = Message.LOGIN_DISABLED
            else:
                message = Message.LOGIN_INVALID

        return render(self.request, self.template_name, {'error': message, 'form': form})


class SignupView(View):
    template_name = 'authentication/signup.html'
    form_class = SignupForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('authentication:welcome'))

        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('authentication:welcome'))
        
        form = self.form_class(request.POST)
        context = {'form': form}
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if password == confirm_password:
                user.set_password(password)
                user.save()
                return redirect(reverse('authentication:login') + '?username=' + username)
            else:
                context['error'] = 'Passwords fields are not matching, Please fill password fields carefully'
        return render(request, self.template_name, context)


class WelcomeView(View):
    template_name = 'authentication/welcome.html'

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    def dispatch(self, *args, **kwargs):
        return super(WelcomeView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'username': request.user.username})


class LogoutView(View):
    template_name = 'authentication/login.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('authentication:login'))
