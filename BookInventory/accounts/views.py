# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from accounts.models import UserModel


def signup(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            if username and password:
                user = UserModel.objects.create(username=username)
                user.set_password(password)
                user.save()
                return HttpResponseRedirect('./login')
            else:
                context['error_username'] = "Username or Passoword cannot be empty"
        except IntegrityError as e:
            context['error_username'] = "Username Already Exist"
    return render(request, 'accounts/signup.html', context)


@login_required
def profile(request):
    if request.user.is_authenticated:
        user = get_object_or_404(UserModel, username=request.user)
        context = {'user': user}
        return render(request, 'accounts/profile.html', context)


def update_profile(request):
    user = get_object_or_404(UserModel, username=request.user)
    if request.method == 'POST':
        user.first_name = request.POST.get('fname', None)
        user.last_name = request.POST.get('lname', None)
        user.email = request.POST.get('email', None)
        user.address = request.POST.get('address', None)
        user.contact = request.POST.get('contact', None)
        user.timezone = request.POST.get('timezone', None)
        if request.FILES:
            user.image = request.FILES['image']
        user.save()
        return redirect("books:index")
    else:
        user = get_object_or_404(UserModel, username=request.user)
        context = {'user': user}
        return render(request, 'accounts/profile_update.html', context)
