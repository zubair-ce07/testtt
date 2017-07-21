from requests import Response

from django.http import Http404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from UserRegistration.models import CustomUser, Task
from .serializers import UserSerializer, UsersTaskSerializer


class UsersTaskListCreateView(generics.ListCreateAPIView):
    """
    View for creating and listing tasks for user

    Attributes:
        serializer_class: Being equal to UserTaskSerializer
        permission_classes: Permissions that would be checked before giving the response to the user
    """
    serializer_class = UsersTaskSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    def perform_create(self, serializer):
        """
        Create task for incoming request user
        Note: The default perform_create() method is overwritten

        Args:
            serializer: The serializer that should be used
        """
        if self.request.user.is_superuser:
            user_id = self.request.POST.get('user')
            if user_id is not None:
                try:
                    CustomUser.objects.get(email=user_id)
                except CustomUser.DoesNotExist:
                    raise Http404('User Not Found')
                if serializer.is_valid():
                    serializer.save(user=CustomUser.objects.get(email=user_id))
                    return
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_superuser:
            return Task.objects.all().order_by('name')
        return Task.objects.filter(user=user)


class UserTaskDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    View to get, edit, and destroy given task
    """
    queryset = Task.objects.all()
    serializer_class = UsersTaskSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)


class CustomUserList(viewsets.ModelViewSet):
    """
    View for creating and listing users using inherited ModelViewSet

    Attributes:
        serializer_class: Being equal to UserTaskSerializer
        permission_classes: Permissions that would be checked before giving the response to the user
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_superuser:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=user.id)


class GetUpdateDeleteUserAPIView(APIView):
    """
    View to get, edit and destroy current user details

    Attributes:
        permission_classes: Permissions that would be checked before giving the response to the user
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """Retrieve the requested user"""
        user = request.user
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)

    def patch(self, request):
        """Partially update the requested user's profile"""
        user = request.user
        user_serializer = UserSerializer(user, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """Delete the requested user"""
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request):
        """Completely update the requested user's profile"""
        user = request.user
        user_serializer = UserSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
