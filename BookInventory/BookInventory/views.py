from __future__ import unicode_literals

from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render

from books.models import UserModel


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
    return render(request, 'registration/signup.html', context)
