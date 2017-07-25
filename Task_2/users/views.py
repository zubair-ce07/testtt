from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from users.decorators import login_required
from users.forms import LoginForm, SignupForm, EditForm
from users.models import UserProfile


@login_required
def DetailsView(request):
    return render(request, 'users/details.html', {'user': request.user})


@login_required
def EditView(request):
    user = request.user
    userprofile = user.userprofile
    data = {'phone_number': userprofile.phone_number, 'address': userprofile.address,
            'image': userprofile.image, 'country': userprofile.country}
    if request.method == 'GET':
        form = EditForm(None, instance=user, initial=data, FILES=request.FILES)
    else:
        form = EditForm(request.POST, instance=user, initial=data, FILES=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(redirect_to=reverse('users:details'))
    return render(request, 'users/edit.html', {'form': form})


def SignUpView(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to=reverse('users:details'))
    if request.method == 'GET':
        form = SignupForm()
    else:
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = UserProfile.objects.create(
                user=User.objects.create(username=form.cleaned_data['username'],
                                         password=make_password(form.cleaned_data['password']),
                                         email=form.cleaned_data['email'],
                                         first_name=form.cleaned_data.get('first_name', None),
                                         last_name=form.cleaned_data.get('last_name', None)),
                phone_number=form.cleaned_data.get('phone_number', None),
                country=form.cleaned_data.get('country', None),
                address=form.cleaned_data.get('address', None),
                image=request.FILES.get('image', None))
            request.session['userid'] = str(user_profile.user.id)
            login(request, user_profile.user)
            return HttpResponseRedirect(redirect_to=reverse('users:details'))
    return render(request, 'users/signup.html', {'form': form})


def LoginView(request):
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user and user.is_active:
                request.session['userid'] = str(user.id)
                login(request, user)
                if 'next' in request.GET and request.GET['next'] != settings.LOGIN_URL:
                    return redirect(request.GET['next'])
                return redirect('users:details')
    return render(request, 'users/login.html', {'form': form})


def LogoutView(request):
    logout(request)
    if 'next' in request.GET:
        return redirect(reverse('users:login') + '?next=' + request.GET['next'])
    return redirect('users:login')
