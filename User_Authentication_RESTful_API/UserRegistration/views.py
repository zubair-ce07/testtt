from requests import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import UsersTaskSerializer, CustomUsersSerializer
from rest_framework import generics, status
from .models import CustomUser, Task
from rest_framework import permissions
from UserRegistration.permission import IsUserOrAdmin


class UsersTaskList(generics.ListCreateAPIView):
    serializer_class = UsersTaskSerializer
    permission_classes = (permissions.IsAuthenticated, IsUserOrAdmin)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_superuser:
            return Task.objects.all()
        return Task.objects.filter(user=user)


class UserTaskDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = UsersTaskSerializer
    permission_classes = (permissions.IsAuthenticated, IsUserOrAdmin,)


class CustomUserList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUsersSerializer
    permission_classes = (permissions.IsAdminUser,)

    def perform_create(self, serializer):
        serializer.save()


class GetCurrentUserDetails(APIView):
    """Get User Detail"""
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        user = request.user
        user_serializer = CustomUsersSerializer(user)
        return Response(data=user_serializer.data, status=status.HTTP_200_OK)


class GetUpdateDeleteUserAPIView(APIView):

    def get(self, request, format=None):
        user = request.user
        serializer = CustomUsersSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = request.user
        serializer = CustomUsersSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, format=None):
        user = request.user
        serializer = CustomUsersSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)