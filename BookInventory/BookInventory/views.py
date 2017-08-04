from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm

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
        user.address = "lhr"
        user.save()
        return HttpResponseRedirect('./login')
    else:
        return render(request, 'registration/signup.html')
