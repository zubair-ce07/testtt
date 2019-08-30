"""core view module"""
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

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
    """User registration view for api
    post request format
    {
        "username":"USERNAME",
        "password1":"password",
        "password2":"password",
        "user_type":"shop or customer"
    }
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        """post method for api user registration"""
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')
        user_type = request.data.get('user_type')
        if password1 != password2:
            return Response(data="Password not match", status=status.HTTP_400_BAD_REQUEST)
        if user_type in ('customer', 'shop'):
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(data={'user': serializer.data, 'user_type': user_type}, status=status.HTTP_200_OK)
        return Response(
            data="User type not valid! only customer and shop are allowed",
            status=status.HTTP_400_BAD_REQUEST
        )


class ApiUserLogin(ObtainAuthToken):
    """User login view for api.
    post request format
    {
        "username":"username",
        "password":"password"
    }
    """

    def post(self, request, *args, **kwargs):
        """post method for ApiUserLogin"""
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)
        return Response(data={'token': token.key, 'user': user_serializer.data}, status=status.HTTP_200_OK)


class ApiUserLogout(APIView):
    """User logout view for api."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        """get method for api user logout"""
        request.user.auth_token.delete()
        return Response(data={"message": "loggedout sucessfully"}, status=status.HTTP_200_OK)
