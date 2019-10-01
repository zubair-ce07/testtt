from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from .models import User


@csrf_exempt
@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if not email and password:
        return Response({'error': 'Please provide both email and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(email=email, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    user = {
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'gender': user.gender,
        'date_of_birth': user.date_of_birth
    }
    return Response({'token': token.key, 'user': user},
                    status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def signup(request):
    email = request.data.get("email")
    password = request.data.get("password")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    date_of_birth = request.data.get("date_of_birth")
    gender = request.data.get("gender")
    if not any([email, password, first_name, last_name, date_of_birth, gender]):
        return Response({'error': 'Please provide all the credentials'},
                        status=HTTP_400_BAD_REQUEST)
    try:
        User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            gender=gender
        )
    except Exception:
        return Response({'error': 'invalid credentials'}, status=HTTP_400_BAD_REQUEST)
    user = authenticate(email=email, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)

    user = {
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'gender': user.gender,
        'date_of_birth': user.date_of_birth
    }
    return Response({'token': token.key, 'user': user},
                    status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def logout(request):
    token = request.data.get("token")
    if not token:
        return Response({'error': 'Invalid credentials'},
                        status=HTTP_400_BAD_REQUEST)
    token = Token.objects.get(key=token)
    user = Token.objects.get(key=token).user
    token.delete()
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=HTTP_200_OK)

