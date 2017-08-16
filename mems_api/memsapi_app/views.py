from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from memsapi_app.models import User, Memory, Activity, Category
from memsapi_app.serializers import UserSerializer, MemorySerializer, LoginSerializer,\
                                    ActivitySerializer, CategorySerializer
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response


def index(request):
    return render(request, 'memsapi_app/index.html', {})


# just for test in React App
class GetAllMems(generics.ListAPIView):
    authentication_classes = ()
    permission_classes = (AllowAny, )
    queryset = Memory.objects.all()
    serializer_class = MemorySerializer


class Login(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        login_serializer = self.serializer_class(data=request.data)
        if login_serializer.is_valid():
            user = authenticate(request, email=data['email'], password=data['password'])
            if user:
                user = User.objects.get(email=user)
                token = Token.objects.get_or_create(user=user)
                key = str(token[0])
                return Response({'token': key})
            else:
                return HttpResponse("User name or password is not valid")
        return JsonResponse(login_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class UserView(generics.CreateAPIView, generics.RetrieveUpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateAndListCategory(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        self.queryset = request.user.categories
        return super(CreateAndListCategory, self).get(request, *args, **kwargs)

    """
    Override to add user in request data on the base 
    of current authentication token
    """
    def post(self, request, *args, **kwargs):
        mutable = request.data._mutable
        request.data._mutable = True
        request.data['user'] = request.user.id
        request.data._mutable = mutable
        return super(CreateAndListCategory, self).post(request, *args, **kwargs)


class ActivityListView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    """
    Override to get list of current user's activities
    """
    def get(self, request, *args, **kwargs):
        self.queryset = request.user.activities
        return super(ActivityListView, self).get(request, *args, **kwargs)


class MemoryListView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Memory.objects.all()
    serializer_class = MemorySerializer

    def get(self, request, *args, **kwargs):
        self.queryset = request.user.mems
        return super(MemoryListView, self).get(request, *args, **kwargs)

    """
    Override to add user in request data on the base 
    of current authentication token
    """
    def post(self, request, *args, **kwargs):
        mutable = request.data._mutable
        request.data._mutable = True
        request.data['user'] = request.user.id
        request.data._mutable = mutable
        return super(MemoryListView, self).post(request, *args, **kwargs)


class GetPublicMems(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Memory.public_memories.all()
    serializer_class = MemorySerializer