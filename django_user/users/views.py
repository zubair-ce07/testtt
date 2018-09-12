from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .forms import (
    UserSignUpForm,
    UserChangePasswordForm,
    UserEditProfileForm,
    UserSignInForm
)
from .models import User


def user_signup_view(request):
    if 'my_session' in request.session:
        user_signout_view(request)

    context = {}
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if check_user_presence(username):
                context = {
                    'message': 'Username ({}) has already exist.'.format(username)
                }
            else:
                obj = User.objects.create(
                    username=form.cleaned_data.get('username'),
                    password=form.cleaned_data.get('password'),
                    date_of_birth=form.cleaned_data.get('date_of_birth')
                )
                context = {
                    'message': "You have signed up successfullty."
                }
            template_name = 'users/signup.html'
            return render(request, template_name, context)

        context = {
            'message': ("Sign Up Failed\nPlease check all the fields")
        }
    template_name = 'users/signup.html'
    return render(request, template_name, context)


def user_signin_view(request):
    if 'my_session' in request.session:
        return HttpResponseRedirect(reverse('users:home'))

    if request.method == 'POST':
        form = UserSignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            obj = User.objects.filter(
                username=username,
                password=form.cleaned_data.get('password'),
            )
            if obj:
                request.session["my_session"] = obj[0].username
                return HttpResponseRedirect(reverse('users:home'))
            if check_user_presence(username):
                context = {
                    'message': 'You have entered wrong password.'
                }
            else:
                context = {
                    'message': 'Username not found.'
                }
        else:
            context = {
                'message': 'Sign in failed. Please check all the fields'
            }
        template_name = 'users/signin.html'
        return render(request, template_name, context)

    template_name = 'users/signin.html'
    context = {}
    return render(request, template_name, context)


def user_signout_view(request):
    request.session.pop('my_session', None)
    return HttpResponseRedirect(reverse('users:signin'))


def user_home_view(request):
    if 'my_session' not in request.session:
        return HttpResponseRedirect(reverse('users:signin'))
    context = {}
    template_name = 'users/home.html'
    return render(request, template_name, context)


def user_change_password_view(request):
    if 'my_session' not in request.session:
        return HttpResponseRedirect(reverse('users:signin'))
    if request.method == 'POST':
        form = UserChangePasswordForm(request.POST)
        if form.is_valid():
            obj = User.objects.filter(
                username=request.session['my_session'],
                password=form.cleaned_data.get('old_password'),
            )
            if obj:
                obj[0].password = form.cleaned_data.get('new_password')
                obj[0].save()
                return HttpResponseRedirect(reverse('users:signin'))
        return HttpResponseRedirect(reverse('users:home'))

    template_name = 'users/change_password.html'
    context = {}
    return render(request, template_name, context)


def user_edit_profile_view(request):
    if 'my_session' not in request.session:
        return HttpResponseRedirect(reverse('users:signin'))

    if request.method == 'POST':
        form = UserEditProfileForm(request.POST)
        if form.is_valid():
            obj = User.objects.filter(
                username=request.session['my_session']
            )
            if obj:
                save_object_data(obj, form)
                return HttpResponseRedirect(reverse('users:home'))
        return HttpResponseRedirect(reverse('users:home'))

    context = {}
    obj = User.objects.filter(
        username=request.session['my_session']
    )
    if obj:
        context = populate_object_data_in_context(context, obj)
    template_name = 'users/edit_profile.html'
    return render(request, template_name, context)


def save_object_data(obj, form):
    obj[0].first_name = form.cleaned_data.get('first_name')
    obj[0].last_name = form.cleaned_data.get('last_name')
    obj[0].city = form.cleaned_data.get('city')
    obj[0].country = form.cleaned_data.get('country')
    obj[0].qualification = form.cleaned_data.get('qualification')
    obj[0].date_of_birth = form.cleaned_data.get('date_of_birth')
    obj[0].save()


def populate_object_data_in_context(context, obj):
    context['password'] = obj[0].password if obj[0].password else ''
    context['first_name'] = obj[0].first_name if obj[0].first_name else ''
    context['last_name'] = obj[0].last_name if obj[0].last_name else ''
    context['city'] = obj[0].city if obj[0].city else ''
    context['country'] = obj[0].country if obj[0].country else ''
    context['qualification'] = obj[0].qualification if obj[0].qualification else ''
    my_date = obj[0].date_of_birth
    date_of_birth = '{}-{:02}-{:02}'.format(my_date.year, my_date.month, my_date.day)
    context['date_of_birth'] = date_of_birth
    return context


def check_user_presence(username):
    if User.objects.filter(username=username):
        return True
    return False
