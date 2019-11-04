from django.core.exceptions import PermissionDenied
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (BasePermission, IsAdminUser,
                                        IsAuthenticated)
from rest_framework.response import Response

from profile_management.api.serializers import (CustomUserSerializer,
                                                SignUpSerializer)
from profile_management.models import CustomUser


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_users(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    users = CustomUser.objects.filter(is_superuser=False)
    result_page = paginator.paginate_queryset(users, request)
    serializer = CustomUserSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request, pk):
    """Retrieve a user."""
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CustomUserSerializer(user)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request, pk):
    """Update a user."""
    try:
        user = CustomUser.objects.get(pk=pk)
        # From Docs: Function-based views will need to check object permissions
        #  explicitly, raising PermissionDenied on failure

        # Check if current user is admin or user itself
        if not (request.user.is_superuser) and user.pk != request.user.pk:
            raise PermissionDenied()
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = {}
    serializer = CustomUserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        data['success'] = "Update successful"
        return Response(data=data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_user(request, pk):
    """Delete a user."""
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = {}
    if user.delete():
        data['success'] = "Delete successful"
    else:
        data['failure'] = "Delete failed"
    return Response(data=data, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def create_user(request):
    """User Sign up"""
    serializer = SignUpSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        data['user'] = CustomUserSerializer(user).data
        data['user']['token'] = Token.objects.get(user=user).key
    else:
        data = serializer.errors
    return Response(data)
