from __future__ import unicode_literals
from django.shortcuts import render
from connect.forms import UserCreationForm, EditProfileForm
from django.template.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def viewprofile(request):
        user = request.user
        return render(request, 'connect/view_profile.html', {"user": user})

def editprofile(request):
    user = request.user
    form = EditProfileForm(request.POST or None, initial={'first_name': user.first_name, 'last_name': user.last_name,
                                                          'email': user.email})
    if request.method == 'POST':
        if form.is_valid():
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()
            return HttpResponseRedirect(reverse('profile'))
    context = {
        "form": form
    }
    return render(request, "connect/edit_profile.html", context)

def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return render(request, 'connect/view_profile.html', {"user": user})
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    return render_to_response('connect/signup.html', args)