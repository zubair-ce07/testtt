from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.contrib.auth.models import User

from registration.models import CustomUser, UserProfile
from task1.forms import UserLoginForm, UserCreateForm
from registration.forms import EditUserProfileForm


def SignUpView(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to=reverse('registration:details'))
    if request.method == 'GET':
        userform = UserCreateForm()
        userprofileform = EditUserProfileForm()
    else:
        userform = UserCreateForm(request.POST)
        userprofileform = EditUserProfileForm(request.POST, request.FILES)
        if userform.is_valid() and userprofileform.is_valid():
            up = UserProfile.objects.create(user=User.objects.create(username=userform.cleaned_data['username'],
                                                                     password=make_password(
                                                                         userform.cleaned_data['password1'])),
                                            phone_number=userprofileform.cleaned_data.get('phone_number', None),
                                            country=userprofileform.cleaned_data.get('country', None),
                                            address=userprofileform.cleaned_data.get('address', None),
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
    return render(request, 'accounts/signup.html', {'userform': userform, 'userprofileform': userprofileform})


def LoginView(request):
    if request.method == 'GET':
        userform = UserLoginForm()
    else:
        userform = UserLoginForm(request.POST)
        if userform.is_valid():
            user = authenticate(username=userform.cleaned_data['username'], password=userform.cleaned_data['password'])
            if user and user.is_active:
                request.session['userid'] = str(user.id)
                login(request, user)
                return HttpResponseRedirect(redirect_to=reverse('registration:details'))
    return render(request, 'accounts/login.html', {'userform': userform})


def LogoutView(request):
    logout(request)
    return HttpResponseRedirect(redirect_to=reverse('login'))
