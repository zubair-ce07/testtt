"""Core view module."""
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

from core.serializers import RegisterUserSerializer
from core.forms import UserRegisterForm
from core.constants import USER_TYPE, SALOON, CUSTOMER, PASSWORD1, PASSWORD2
from shop.models import Saloon
from customer.models import Customer


class LogoutView(View):
    """Log out User view."""

    @staticmethod
    def get(request):
        """Log out User and clear it's session and cookies."""
        auth_logout(request)
        return redirect('login')


class UserRegisterView(View):
    """Render and save shop user.

    This method renders the user registration form and also save it's data
    when form is submitted.
    """

    @staticmethod
    def post(request):
        """User Register View POST method."""
        user_form = UserRegisterForm(request.POST)
        user_type = request.POST.get(USER_TYPE, None)
        if user_form.is_valid():
            user = user_form.save()
            if user_type == CUSTOMER:
                Customer.objects.create(user=user)
            elif user_type == SALOON:
                Saloon.objects.create(user=user)

            messages.success(request, f'Your account has been Created!')
            return redirect('login')
        return render(request, 'core/register.html', {'user_form': user_form})

    @staticmethod
    def get(request):
        """User Register View GET method."""
        user_form = UserRegisterForm()
        return render(request, 'core/register.html', {'user_form': user_form})


class UserRegisterationApiView(generics.CreateAPIView):
    """User registration view for api.

    post request format
    {
        "username":"USERNAME",
        "password1":"password",
        "password2":"password",
        "user_type":"saloon or customer"
    }
    """

    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        """Post method for api user registration."""
        password1 = request.data.get(PASSWORD1)
        password2 = request.data.get(PASSWORD2)
        user_type = request.data.get(USER_TYPE)
        if password1 != password2:
            return Response(data="Password does not match", status=status.HTTP_400_BAD_REQUEST)
        if user_type in (CUSTOMER, SALOON):
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(data={'user': serializer.data, 'user_type': user_type}, status=status.HTTP_200_OK)
        return Response(
            data='User type not valid! only customer and shop are allowed',
            status=status.HTTP_400_BAD_REQUEST
        )


class UserLoginApiView(ObtainAuthToken):
    """User login view for api.

    post request format
    {
        "username":"username",
        "password":"password"
    }
    """

    def post(self, request, *args, **kwargs):
        """Post method for ApiUserLogin."""
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        user_serializer = RegisterUserSerializer(user)
        if hasattr(user, SALOON):
            user_type = SALOON
        elif hasattr(user, CUSTOMER):
            user_type = CUSTOMER
        else:
            user_type = 'none'
        context = {'token': token.key,
                   'user': user_serializer.data, 'user_type': user_type}
        return Response(data=context, status=status.HTTP_200_OK)


class UserLogoutApiView(APIView):
    """User logout view for api."""

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        """Get method for api user logout."""
        request.user.auth_token.delete()
        return Response(data={'message': 'loggedout sucessfully'}, status=status.HTTP_200_OK)
