from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from locallibrary.forms import UserForm


def signup(request):
    if request.method == 'GET':
        form = UserForm()
        return render(request, 'registration/signup.html', {'form': form})
    user = User()
    form = UserForm(request.POST)
    if form.is_valid():
        user.username = form.cleaned_data['username']
        user.set_password(form.cleaned_data['password'])
        user.save()
        return HttpResponseRedirect(redirect_to='/')
    return render(request, 'registration/signup.html', {'form': form})
