from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.contrib.auth.models import User

from registration.models import UserProfile
from task1.forms import UserLoginForm, UserCreateForm
from registration.forms import EditUserProfileForm


def SignUpView(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to=reverse('registration:details'))
    if request.method == 'GET':
        form = UserCreateForm()
        # userprofileform = EditUserProfileForm()
    else:
        form = UserCreateForm(request.POST, request.FILES)
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
            # user = CustomUser(username=userform.cleaned_data['username'],
            #                   password=make_password(userform.cleaned_data['password1']))
            # user.save(phone_number=userprofileform.cleaned_data.get('phone_number', None),
            #           image=request.FILES.get('image', None),
            #           country_name=userprofileform.cleaned_data.get('country', None),
            #           address=userprofileform.cleaned_data.get('address', None))
            request.session['userid'] = str(up.user.id)
            login(request, up.user)
            return HttpResponseRedirect(redirect_to=reverse('registration:details'))
    return render(request, 'accounts/signup.html', {'form': form})


def LoginView(request):
    if request.method == 'GET':
        form = UserLoginForm()
    else:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user and user.is_active:
                request.session['userid'] = str(user.id)
                login(request, user)
                return HttpResponseRedirect(redirect_to=reverse('registration:details'))
    return render(request, 'accounts/login.html', {'form': form})


def LogoutView(request):
    logout(request)
    return HttpResponseRedirect(redirect_to=reverse('login'))
