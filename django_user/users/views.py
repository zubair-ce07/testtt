from django.shortcuts import render
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

    template_name = 'users/signin.html'
    context = {}
    if request.method == 'POST':
        form = UserSignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:
                obj = User.objects.get(username=username, password=password)
                request.session["my_session"] = obj.username
                return HttpResponseRedirect(reverse('users:home'))
            except User.DoesNotExist:
                if check_user_presence(username):
                    context['message'] = 'You have entered wrong password.'
                else:
                    context['message'] = 'Username not found.'
        else:
            context['message'] = 'Sign in failed. Please check all the fields'
        return render(request, template_name, context)
    return render(request, template_name, context)


def user_signout_view(request):
    if 'my_session' in request.session:
        del request.session['my_session']
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

    context = {}
    template_name = 'users/change_password.html'
    if request.method == 'POST':
        form = UserChangePasswordForm(request.POST)
        if form.is_valid():
            username = request.session['my_session']
            password = form.cleaned_data.get('old_password')
            try:
                obj = User.objects.get(username=username, password=password)
                obj.password=form.cleaned_data.get('new_password')
                obj.save()
                return user_signout_view(request)
            except User.DoesNotExist:
                context['message'] = 'You entered wrong password'
        context['message'] = 'Form Validation Failed'
    return render(request, template_name, context)


def user_edit_profile_view(request):
    if 'my_session' not in request.session:
        return HttpResponseRedirect(reverse('users:signin'))

    context = {}
    template_name = 'users/edit_profile.html'
    username = request.session['my_session']
    if request.method == 'POST':
        form = UserEditProfileForm(request.POST)
        if form.is_valid():
            try:
                obj = User.objects.get(username=username)
                save_object_data(obj, form)
                return HttpResponseRedirect(reverse('users:home'))
            except User.DoesNotExist:
                return user_signout_view()
        context['message'] = 'Form Validation Failed!!!'
        return render(request, template_name, context)

    try:
        obj = User.objects.get(username=username)
        context = populate_object_data_in_context(context, obj)
        return render(request, template_name, context)
    except:
        return user_signout_view()


def save_object_data(obj, form):
    obj.first_name = form.cleaned_data.get('first_name')
    obj.last_name = form.cleaned_data.get('last_name')
    obj.city = form.cleaned_data.get('city')
    obj.country = form.cleaned_data.get('country')
    obj.qualification = form.cleaned_data.get('qualification')
    obj.date_of_birth = form.cleaned_data.get('date_of_birth')
    obj.save()


def populate_object_data_in_context(context, obj):
    context['password'] = obj.password if obj.password else ''
    context['first_name'] = obj.first_name if obj.first_name else ''
    context['last_name'] = obj.last_name if obj.last_name else ''
    context['city'] = obj.city if obj.city else ''
    context['country'] = obj.country if obj.country else ''
    context['qualification'] = obj.qualification if obj.qualification else ''
    my_date = obj.date_of_birth
    date_of_birth = '{}-{:02}-{:02}'.format(my_date.year, my_date.month, my_date.day)
    context['date_of_birth'] = date_of_birth
    return context


def check_user_presence(username):
    try:
        user = User.objects.get(username=username)
        return user
    except:
        return None
