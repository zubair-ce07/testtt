from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .forms import UserCreationForm, UserLoginForm
from .serializers import UserFormSerializer


def index(request):
    return render(request, 'registration/base.html')


@login_required
def home(request):
    return render(request, 'registration/home.html')


def signup(request):
    if request.method == 'POST':
        user_creation_form = UserCreationForm(request.POST)
        user = UserFormSerializer(data=user_creation_form.data)
        if user.is_valid():
            user.create(user.validated_data)
            email = user.validated_data.get('email')
            raw_password = user.validated_data.get('password_')
            user = authenticate(email=email, password=raw_password)
            token = Token.objects.get_or_create(user=user)[0]
            return render(request, 'registration/home.html', {'token': token.key})

    else:
        user_creation_form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': user_creation_form})


def login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            email = user_login_form.data.get("email")
            password = user_login_form.data.get("password")
            user = authenticate(email=email, password=password)
            if not user:
                return Response('Invalid Credentials')

            token = Token.objects.get_or_create(user=user)[0]
            return render(request, 'registration/home.html', {'token': token.key})
    return render(request, 'registration/login.html', {'form': UserLoginForm()})

