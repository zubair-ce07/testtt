import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import UserForm
from django.contrib.auth.models import User

def signup(request):

    if request.method == 'GET':
        form = UserForm()
        return render(request, 'registration/signup.html', {'form': form})
    else:
        user = User()
        form = UserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user.username = form.cleaned_data['username']
            user.set_password(form.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect(redirect_to='/')
    
    return render(request, 'registration/signup.html', {'form': form})
      

        



    
