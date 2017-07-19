from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import User, UserInfo
from django.views.generic.edit import FormView
from .forms import LoginForm, SignUpForm

import datetime


app_name = 'wblog'


class Login(LoginView):
    authentication_form = LoginForm
    template_name = 'wblog/index.html'
    redirect_authenticated_user = True


class Profile(FormView):
    template_name = 'wblog/profile.html'


class Logout(LogoutView):
    next_page = 'wblog/index.html'


class SignupView(FormView):
    template_name = 'wblog/signup.html'
    form_class = SignUpForm
    success_url = '/welcome/'

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        print(form)
        if form.is_valid():
            user = User(username=form.cleaned_data['username'],
                        password=form.cleaned_data['password']
                        )
            user.info = {'phone_num': form.cleaned_data['phone_no'],
                         'address': form.cleaned_data['address'],
                         'dob': form.cleaned_data['date_of_birth'],
                         'gender': form.cleaned_data['gender'],
                         'created_at': datetime.datetime.now()
                         }
            user.save()
            user = authenticate(username=user.username, password=user.password)
            login(request, user)

            return HttpResponseRedirect(reverse('wblog:login'))

        else:
            return render(request, 'wblog/signup.html', {'form': form})


def profile_view(request):
    user = UserInfo.objects.get(user=request.user)
    if request.method == 'POST':
        print(request.POST)
        form = SignUpForm(request.POST, instance=user)
        form.save(commit=True)
    else:
        print(request.user)
        form = SignUpForm(initial={'username': request.user.username,
                                   'password': request.user.password,
                                   'phone_no': user.phone_no,
                                   'address': user.address,
                                   'date_of_birth': user.date_of_birth,
                                   'gender': user.gender
                                   })
    return render(request, 'wblog/profile.html', {'user': form})
