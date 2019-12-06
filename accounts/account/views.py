from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import EditProfile, LoginForm


@login_required
def login_view(request):
    next = request.GET.get("next")
    form = LoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)

        if next:
            return redirect(next)

        return redirect('/')

    return render(request, "login.html", {'form': form})

def successful_login(request):
    return render(request, "successful_login.html")

def editprofile(request):

    if request.method == "POST":
        form = EditProfile(request.POST, instance=request.user)

        if form.is_valid():
            form.save()

            return redirect("/account/login")

    else:
        form = EditProfile(instance=request.user)
        context = {'form': form}
        return render(request, "edit_profile.html", context)


def changepassword(request):

    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)

            return redirect("/account/login")

        else:
            return redirect("/account/change_password")

    else:
        form = PasswordChangeForm(user=request.user)
        context = {'form': form}
        
        return render(request, "change_password.html", context)
