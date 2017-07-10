from __future__ import unicode_literals
from django.shortcuts import render
from ehub.forms import SignUpForm, LoginForm, EditProfileForm
from django.template.context_processors import csrf
from django.contrib.auth import authenticate, login as session_login, logout as session_logout
from django.views.generic import UpdateView


def viewprofile(request):
    user = request.user
    return render(request, 'ehub/view_profile.html', {"user": user})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return render(request, 'ehub/view_profile.html', {"user": user})
        elif form.errors:
            for field in form:
                for error in field.errors:
                    print(error)
    args = {}
    args.update(csrf(request))
    args['form'] = SignUpForm()
    return render(request, 'ehub/signup.html', args)


def login(request):
    if request.method == 'POST':
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                session_login(request, user)
                return render(request, 'ehub/view_profile.html', {'user': user})

    args = {}
    args.update(csrf(request))
    args['form'] = LoginForm()
    return render(request, 'ehub/login.html', args)


def logout(request):
    session_logout(request)


class EditProfile(UpdateView):
    form_class = EditProfileForm
    template_name = 'editprofile_form.html'
    success_url = '/ehub/profile/'

    def get_object(self, queryset=None):
        return self.request.user
