from django.contrib.auth import authenticate, logout
from django.db import transaction
from django.http import QueryDict
from django.shortcuts import redirect, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework_jwt.serializers import JSONWebTokenSerializer

from api.serializers import UserSerializer, EditSerializer, SignupSerializer, UserListSerializer, UPSerializer
from users.models import UserProfile


def get_token(request):
    req_data = {'csrfmiddlewaretoken': request.data.get('csrfmiddlewaretoken'),
                'username': request.data.get('username'),
                'password': request.data.get('password1')}
    data = QueryDict('', mutable=True)
    data.update(req_data)
    token = JSONWebTokenSerializer(data=data)
    if token.is_valid():
        return token.validated_data.get('token')


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('api:list', request=request, format=format),
    }, status=status.HTTP_200_OK)


class UserList(APIView):
    """
    Endpoint for Users
    """

    def get(self, request, format=None):
        users = UserProfile.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        request.META['Authorization'] = 'JWT ' + get_token(request)
        serializer = UserListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
    Endpoint for a single User profile
    """

    def get_object(self):
        return get_object_or_404(UserProfile, user__id=self.request.user.id)

    def get(self, request, format=None):
        user = self.get_object()
        serializer = UserListSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        user = self.get_object()
        serializer = UserListSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserProfileDetails(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/details.html'

    def get(self, request):
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=request.user)
            serializer = UPSerializer(user_profile)
            return Response({'user': user_profile.user, 'serializer': serializer.data}, status=status.HTTP_200_OK)
        return redirect('api:login')


class UserProfileEdit(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/edit.html'

    def get(self, request):
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=request.user)
            serializer = EditSerializer(user_profile)
            return Response({'serializer': serializer}, status=status.HTTP_200_OK)
        return redirect('api:login')

    def post(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = EditSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('api:details')
        return Response({'serializer': serializer}, status=status.HTTP_400_BAD_REQUEST)


class SignupView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/signup.html'
    permission_classes = (AllowAny,)

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('api:details')
        serializer = SignupSerializer()
        return Response({'serializer': serializer}, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = redirect('api:details')
            response.set_cookie('token', get_token(request))
            return response
        return Response({'serializer': serializer}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/login.html'
    permission_classes = (AllowAny,)

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('api:details')
        serializer = UserSerializer()
        return Response({'serializer': serializer}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data.get('username'),
                                password=serializer.validated_data.get('password'))
            if user and user.is_active:
                return redirect('api:details')
        return Response({'serializer': serializer}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def get(self, request):
        logout(request)
        request.COOKIES.clear()
        response = redirect('api:login')
        response.delete_cookie('token')
        return response
