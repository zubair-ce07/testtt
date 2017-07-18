<<<<<<< HEAD
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from .models import User
from django.views.generic.edit import FormView
from .forms import LoginForm, SignUpForm

import datetime


app_name = 'wblog'


class Login(LoginView):
    authentication_form = LoginForm
    template_name = 'wblog/index.html'


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
=======
from django.shortcuts import render

# Create your views here.
>>>>>>> d6e8908... Adding Main Models
