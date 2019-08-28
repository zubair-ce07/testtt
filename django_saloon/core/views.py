"""core view module"""
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.views import APIView

from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.serializers import UserSerializer
from core.forms import UserRegisterForm
from shop.models import Saloon
from customer.models import Customer


class LogoutView(View):
    """Log out User view."""

    @staticmethod
    def get(request):
        """Log out User and clear it's session and cookies.
        """
        auth_logout(request)
        return redirect('login')


class UserRegisterView(View):
    """Render and save shop user

    This method renders the user registration form and also save it's data
    when form is submitted
    """
    @staticmethod
    def post(request):
        """UserRegisterView POST method."""
        user_form = UserRegisterForm(request.POST)
        user_type = request.POST.get("user_type", None)
        if user_form.is_valid():
            user = user_form.save()
            if user_type == 'customer':
                Customer.objects.create(user=user)
            else:
                Saloon.objects.create(user=user)

            messages.success(request, f'Your account has been Created!')
            return redirect('login')
        return render(request, 'core/register.html', {'user_form': user_form})

    @staticmethod
    def get(request):
        """UserRegisterView GET method."""
        user_form = UserRegisterForm()
        return render(request, 'core/register.html', {'user_form': user_form})


class ApiUserRegisteration(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')
        if password1 != password2:
            return Response(data="Password not match", status=400)
        return super().post(request, *args, **kwargs)


class ApiUserLogout(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        request.user.auth_token.delete()
        return Response({"message": "loggedout sucessfully"})
