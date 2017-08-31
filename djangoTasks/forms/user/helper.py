import json

from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.shortcuts import render


def username_exist(request):
    username = request.GET.get('username', None)
    if get_user_model().objects.filter(username=username).exists():
        context = {
            "status": True,
            "message": "User with this username aleady exist"
        }
        return HttpResponse(json.dumps(context))
    context = {
        "status": False,
        "message": "User with this username does not exist"
    }
    return HttpResponse(json.dumps(context))


def email_exist(request):
    email = request.GET.get('email', None)
    if get_user_model().objects.filter(email=email).exists():
        context = {
            "status": True,
            "message": "User with this email aleady exist"
        }
        return HttpResponse(json.dumps(context))
    context = {
        "status": False,
        "message": "User with this email does not exist"
    }
    return HttpResponse(json.dumps(context))
