# -*- coding: utf-8 -*-
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.views import View

from .forms import SignUpForm


class Signup(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
        else:
            form = SignUpForm()
        return render(request, 'signup.html', {'form': form})
