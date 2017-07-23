from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from user.decorators import login_required
from user.models import UserProfile
from user.forms import LoginForm, SignupForm, EditForm


@login_required
def DetailsView(request):
    return render(request, 'user/details.html', {'user': request.user})


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
            return HttpResponseRedirect(redirect_to=reverse('user:details'))
    return render(request, 'user/edit.html', {'form': form})


def SignUpView(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to=reverse('user:details'))
    if request.method == 'GET':
        form = SignupForm()
    else:
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            up = UserProfile.objects.create(
                user=User.objects.create(username=form.cleaned_data['username'],
                                         password=make_password(form.cleaned_data['password1']),
                                         email=form.cleaned_data['email'],
                                         first_name=form.cleaned_data.get('first_name', None),
                                         last_name=form.cleaned_data.get('last_name', None)),
                phone_number=form.cleaned_data.get('phone_number', None),
                country=form.cleaned_data.get('country', None),
                address=form.cleaned_data.get('address', None),
                image=request.FILES.get('image', None))
            request.session['userid'] = str(up.user.id)
            login(request, up.user)
            return HttpResponseRedirect(redirect_to=reverse('user:details'))
    return render(request, 'user/signup.html', {'form': form})


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
                return HttpResponseRedirect(redirect_to=reverse('user:details'))
    return render(request, 'user/login.html', {'form': form})


def LogoutView(request):
    logout(request)
    return HttpResponseRedirect(redirect_to=reverse('user:login'))
