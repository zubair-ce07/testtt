import datetime
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import User, UserProfile
from django.views.generic.edit import FormView
from .forms import LoginForm, SignUpForm


class Login(LoginView):
    authentication_form = LoginForm
    template_name = 'wblog/index.html'


class Profile(FormView):
    template_name = 'wblog/profile.html'


class Logout(LogoutView):
    next_page = '/wblog'


class SignupView(FormView):
    template_name = 'wblog/signup.html'
    form_class = SignUpForm

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
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
        return render(request, 'wblog/signup.html', {'form': form})


def profile_view(request):
    user = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = SignUpForm(request.POST, instance=user)
        user.image = request.FILES['image']
        user.save()
    else:
        form = SignUpForm(initial={'username': request.user.username,
                                   'password': request.user.password,
                                   'phone_no': user.phone_no,
                                   'address': user.address,
                                   'date_of_birth': user.date_of_birth,
                                   'gender': user.gender,
                                   'image': user.image
                                   })
    return render(request, 'wblog/profile.html', {'user': form})
