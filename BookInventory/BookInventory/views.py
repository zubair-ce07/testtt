from __future__ import unicode_literals

from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render

from books.models import UserModel


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = UserModel.objects.create(username=username)
            user.set_password(password)
            user.save()
            return HttpResponseRedirect('./login')
        except IntegrityError as e:
            context = {'error_username': "Username Already Exist"}
            return render(request, 'registration/signup.html', context)
    else:
        return render(request, 'registration/signup.html')
