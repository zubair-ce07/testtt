from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse

from .forms import UserForm


def signup(request):

    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})
    else:
        # user = User()
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            # user.password = make_password(form.cleaned_data['password1']
            raw_password = form.cleaned_data['password1']
            # user.full_clean()
            user = authenticate(username=username, password=raw_password)
            user.save()

            # user.username = form.cleaned_data['username']
            # user.set_password(form.cleaned_data['password1'])
            # user.save()
            return HttpResponseRedirect(redirect_to=reverse('users:details', args=(user.pk,)))

    return render(request, 'registration/signup.html', {'form': form})
