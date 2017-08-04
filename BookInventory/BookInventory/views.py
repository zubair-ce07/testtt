from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from books.models import UserModel


def index(request):
    return redirect('/books')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = UserModel.objects.create()
        user.username = username
        user.set_password(password)
        user.save()
        return HttpResponseRedirect('./login')
    else:
        return render(request, 'registration/signup.html')
