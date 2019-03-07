from django.contrib.auth import get_user_model
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer

User = get_user_model()


class AuthenticateUser(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user, token = User.authenticate(username, password)

        response = {
            'token': token.key,
            'user': UserSerializer(user).data,
        }
        return Response(response)


class RegisterUser(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GetUpdateUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        serializer = UserSerializer(
            request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
