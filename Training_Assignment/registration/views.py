from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.urls import reverse

from registration.forms import EditUserProfileForm, EditUserForm
from task1.decorators import login_required
from registration.models import UserProfile


@login_required
def DetailsView(request):
    return render(request, 'registration/details.html', {'user': request.user})


@login_required
def EditView(request):
    if not request.user:
        return HttpResponseRedirect(redirect_to=reverse('login'))
    user = request.user
    user_profile = user.userprofile
    if request.method == 'GET':
        profileform = EditUserProfileForm(None, instance=user_profile)
        userform = EditUserForm(None, instance=user)
    else:
        profileform = EditUserProfileForm(request.POST, request.FILES, instance=user_profile)
        userform = EditUserForm(request.POST, instance=user)
        if profileform.is_valid() and userform.is_valid():
            profileform.save()
            userform.save()
            return HttpResponseRedirect(redirect_to=reverse('registration:details'))
    return render(request, 'registration/edit.html', {'profileform': profileform, 'userform': userform})


def TestView(request):
    u = UserProfile.objects.create(user=User.objects.create(username='test', password='abcdefgh'),
                                   phone_number='+9111111111')
    # u.save()
    return HttpResponse('worked')
