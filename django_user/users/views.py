from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import UserSignUpInForm, UserChangePasswordForm, UserEditProfileForm
from .models import User


def user_signupview(request):
    try:
        if request.session["my_session"]:
            template_name = 'users/signin.html'
            context = {}
            return render(request, template_name, context)
    except:
        if request.method == 'POST':
            form = UserSignUpInForm(request.POST)
            if form.is_valid():
                obj = User.objects.create(
                    username=form.cleaned_data.get('username'),
                    password=form.cleaned_data.get('password'),
                )
            return HttpResponseRedirect('/users/')
    template_name = 'users/signup.html'
    context = {}
    return render(request, template_name, context)


def user_signinview(request):
    if request.method == 'POST':
        form = UserSignUpInForm(request.POST)
        if form.is_valid():
            obj = User.objects.filter(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password'),
            )
            if obj:
                request.session["my_session"] = obj[0].username
                return HttpResponseRedirect('/users/home/')
        return HttpResponseRedirect('/users/')

    template_name = 'users/signin.html'
    context = {}
    return render(request, template_name, context)


def user_signoutview(request):
    request.session.pop('my_session', None)
    template_name = 'users/signin.html'
    context = {}
    return render(request, template_name, context)


def user_homeview(request):
    context = {}
    try:
        if request.session['my_session'] is not None:
            template_name = 'users/home.html'
            return render(request, template_name, context)
    except:
        pass

    template_name = 'users/signin.html'
    return render(request, template_name, context)


def user_change_passwordview(request):
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
                return HttpResponseRedirect('/users/home/')
        return HttpResponseRedirect('/users/')

    template_name = 'users/change_password.html'
    context = {}
    return render(request, template_name, context)


def user_edit_profileview(request):
    if request.method == 'POST':
        form = UserEditProfileForm(request.POST)
        if form.is_valid():
            obj = User.objects.filter(
                username=request.session['my_session']
            )
            if obj:
                save_object_data(obj, form)
                return HttpResponseRedirect('/users/home/')
        return HttpResponseRedirect('/users/')

    context = {}
    obj = User.objects.filter(
        username=request.session['my_session']
    )
    if obj:
        context['first_name'] = obj[0].first_name
        context['last_name'] = obj[0].last_name
        context['city'] = obj[0].city
        context['country'] = obj[0].country
        context['qualification'] = obj[0].qualification
        context['date_of_birth'] = obj[0].date_of_birth
    template_name = 'users/edit_profile.html'
    return render(request, template_name, context)


def save_object_data(obj, form):
    obj[0].password = form.cleaned_data.get('new_password')
    obj[0].first_name = form.cleaned_data.get('first_name')
    obj[0].last_name = form.cleaned_data.get('last_name')
    obj[0].city = form.cleaned_data.get('city')
    obj[0].country = form.cleaned_data.get('country')
    obj[0].qualification = form.cleaned_data.get('qualification')
    obj[0].date_of_birth = form.cleaned_data.get('date_of_birth')
    obj[0].save()


def populate_object_data_in_context(context, obj):
    context['password'] = obj[0].password
    context['first_name'] = obj[0].first_name
    context['last_name'] = obj[0].last_name
    context['city'] = obj[0].city
    context['country'] = obj[0].country
    context['qualification'] = obj[0].qualification
    context['date_of_birth'] = obj[0].date_of_birth
    return context
