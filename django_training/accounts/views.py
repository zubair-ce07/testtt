from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render


def login(request):
    return render(request, 'accounts\login.html')

def handle_login(request):
    user_name = request.POST['username']
    password = request.POST['password']
    user = authenticate(user_name=user_name, password=password)
    if user:
        return HttpResponse('Successfully Autthenticated')
    else:
        return HttpResponse('<h1>Authentication Error {}: {} </h1>'.format(type(user_name), type(password)))
