from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import api_view
from rest_framework.validators import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework.reverse import reverse

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout

from django.db import transaction

from users.models import UserProfile
from api.serializers import UserSerializer, UserProfileSerializer, SignupSerializer, UserListSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('api:list', request=request, format=format),
    })


class UserList(APIView):
    def get(self, request, format=None):
        users = UserProfile.objects.get(pk=request.user.use)
        serializer = UserListSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    def get_object(self):
        try:
            return UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        user = self.get_object()
        serializer = UserListSerializer(user)
        return Response(serializer.data)

    def put(self, request, format=None):
        user = self.get_object()
        serializer = UserListSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserProfileDetails(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/details.html'

    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        return Response({'user': user_profile.user})


class UserProfileEdit(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/edit.html'

    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile)
        return Response({'serializer': serializer})

    def post(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('api:details')
        return Response({'serializer': serializer})


class SignupView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/signup.html'
    permission_classes = (AllowAny,)

    def get(self, request):
        serializer = SignupSerializer()
        return Response({'serializer': serializer})

    @transaction.atomic
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user_profile = serializer.save()
            login(request, user_profile.user)
            request.session['userid'] = str(user_profile.user.id)
            return redirect('api:details')
        return Response({'serializer': serializer})


class LoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/login.html'
    permission_classes = (AllowAny,)

    def get(self, request):
        serializer = UserSerializer()
        return Response({'serializer': serializer})

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data.get('username'),
                                password=serializer.validated_data.get('password'))
            if user and user.is_active:
                # ojwt = JSONWebTokenSerializer(instance=user, data=request.data)
                # if ojwt.is_valid():
                #     print(ojwt.validated_data)
                request.session['userid'] = str(user.id)
                login(request, user)
                return redirect('api:details')
            return Response({'serializer': serializer})


class LogoutView(APIView):
    def get(self, request):
        logout(request)
        return redirect('api:login')
