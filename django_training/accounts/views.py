from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render

from accounts.forms import LoginForm


def home_page(request):
    return render(request, 'accounts/home.html')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            password = form.cleaned_data['password']
            user = authenticate(username=user_name, password=password)
            if user:
                return HttpResponse('Successfully Autthenticated')
            else:
                return HttpResponse('<h1>Authentication Error {}: {} </h1>'.format(user_name, password))

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})
