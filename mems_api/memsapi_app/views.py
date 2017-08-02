from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from memsapi_app.models import User, Memory, Activity, Category
from memsapi_app.serializers import UserSerializer, MemorySerializer, LoginSerializer,\
                                    ActivitySerializer, CategorySerializer
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class Login(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny, )

    def post(self, request):
        data = JSONParser().parse(request)
        login_serializer = LoginSerializer(data=data)
        if login_serializer.is_valid():
            user = authenticate(request, email=data['email'], password=data['password'])
            if user:
                user = User.objects.get(email=user)
                try:
                    token = Token.objects.create(user=user)
                except:
                    token = Token.objects.get(user_id=user.id)
                return Response({'token': token.key})
            else:
                return HttpResponse("User name or password is not valid")
        return JsonResponse(login_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class CreateUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GetAndUpdateUser(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateAndListCategory(generics.ListCreateAPIView):
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
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    """
    Override to get list of current user's activities
    """
    def get(self, request, *args, **kwargs):
        self.queryset = request.user.activities
        return super(ActivityListView, self).get(request, *args, **kwargs)


class MemoryListView(generics.ListCreateAPIView):
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


class MemoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Memory.objects.all()
    serializer_class = MemorySerializer


class GetPublicMems(generics.ListAPIView):
    queryset = Memory.public_memories.all()
    serializer_class = MemorySerializer