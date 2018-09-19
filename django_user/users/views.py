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
    """ 
    Returns signout view if user alreay logged in.
    Returns signup view if user sends a GET request
    otherwise gets data from the form, validates it
    returns error in case of any error. If validation
    succeeds, creates the user

    """
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
                user = User.objects.create(
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
    """
    Redirects to home view if user is already logged in.
    Returns signin view in case of GET request.
    In case of POST request, gets the data from the 
    form validates it, if validation succeeds, stores
    session and returns home view. Returns error message 
    in case of any failure
    """
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
                user = User.objects.get(username=username, password=password)
                request.session["my_session"] = user.username
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
    """
    Deletes session if it exists and redirects to signin view
    """
    if 'my_session' in request.session:
        del request.session['my_session']
    return HttpResponseRedirect(reverse('users:signin'))


def user_home_view(request):
    """
    Redirects to signin view if session doesnot exist otherwise
    returns home view
    """
    if 'my_session' not in request.session:
        return HttpResponseRedirect(reverse('users:signin'))
    context = {}
    template_name = 'users/home.html'
    return render(request, template_name, context)


def user_change_password_view(request):
    """
    Redirects to signin view if session doesnot exists.
    Returns change password view in case of GET request.
    In case of POST request gets data from form
    validates it using form and changes the password if
    everything goes fine otherwise returns error message    
    """
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
                user = User.objects.get(username=username, password=password)
                user.password = form.cleaned_data.get('new_password')
                user.save()
                return user_signout_view(request)
            except User.DoesNotExist:
                context['message'] = 'You entered wrong password'
        context['message'] = 'Form Validation Failed'
    return render(request, template_name, context)


def user_edit_profile_view(request):
    """
    Redirects to signin view if session doesnot exists.
    Returns edit password view with user's current data
    in case of GET request.In case of POST request gets
    data from form validates it using UserEditProfileForm
    and edits the profile and redirects to home view if 
    everything goes fine otherwise returns error message    
    """
    if 'my_session' not in request.session:
        return HttpResponseRedirect(reverse('users:signin'))

    context = {}
    template_name = 'users/edit_profile.html'
    username = request.session['my_session']
    if request.method == 'POST':
        form = UserEditProfileForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username=username)
                save_object_data(user, form)
                return HttpResponseRedirect(reverse('users:home'))
            except User.DoesNotExist:
                return user_signout_view()
        context['message'] = 'Form Validation Failed!!!'
        return render(request, template_name, context)

    try:
        user = User.objects.get(username=username)
        context = populate_object_data_in_context(context, user)
        return render(request, template_name, context)
    except:
        return user_signout_view()


def save_object_data(user, form):
    """
    Gets data from the form and saves it in the
    user's objects instance
    """
    user.first_name = form.cleaned_data.get('first_name')
    user.last_name = form.cleaned_data.get('last_name')
    user.city = form.cleaned_data.get('city')
    user.country = form.cleaned_data.get('country')
    user.qualification = form.cleaned_data.get('qualification')
    user.date_of_birth = form.cleaned_data.get('date_of_birth')
    user.save()


def populate_object_data_in_context(context, user):
    """
    Gets user data from user's object and saves it in context dictionary
    """
    context['password'] = user.password if user.password else ''
    context['first_name'] = user.first_name if user.first_name else ''
    context['last_name'] = user.last_name if user.last_name else ''
    context['city'] = user.city if user.city else ''
    context['country'] = user.country if user.country else ''
    context['qualification'] = user.qualification if user.qualification else ''
    my_date = user.date_of_birth
    date_of_birth = '{}-{:02}-{:02}'.format(
        my_date.year, my_date.month, my_date.day)
    context['date_of_birth'] = date_of_birth
    return context


def check_user_presence(username):
    """
    Checks either user with the given username exists or not.
    Returns user if it exists otherwise None
    """
    try:
        user = User.objects.get(username=username)
        return user
    except:
        return None
