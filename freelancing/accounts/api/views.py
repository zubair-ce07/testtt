from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.forms.models import model_to_dict

from ..models import User, Profile
from .serliazers import UserSerializer, ProfileSerializer
from .permissions import isSameUser, isAdminOrReadOnly
from freelancing.utils.api.response import \
    invalid_serializer_response, missing_attribute_response, \
    does_not_exists_response


class UserApiList(generics.ListAPIView):
    """Rest api for users
    return a list with a requested user instance in it
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, isAdminOrReadOnly, )

    def list(self, request, *args, **kwargs):
        queryset = User.objects.filter(id=request.user.id)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data[0], status=status.HTTP_200_OK)


class UserApiCreate(generics.CreateAPIView):
    """Rest api for users
    create a user with a required data in the request
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailsApi(generics.RetrieveUpdateDestroyAPIView):
    """Rest api for a single user"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, isSameUser)


class UserRolesApi(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        user = User.objects.filter(id=request.user.id)
        if request.user.is_buyer:
            user.update(is_buyer=False, is_seller=True)
        if request.user.is_seller:
            user.update(is_buyer=True, is_seller=False)

        data = {
            "id": user.get().id,
            "is_buyer": user.get().is_buyer,
            "is_seller": user.get().is_seller
        }

        return Response(data, status=status.HTTP_200_OK)


class UserProfileApi(generics.RetrieveUpdateAPIView):
    """Rest api for a user profile"""

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        queryset = Profile.objects.filter(id=request.user.id)
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data[0], status=status.HTTP_200_OK)

    def get_object(self):
        print(self.request.user)
        obj = self.get_queryset()[0]
        return obj
        
    def update(self, request, *args, **kwargs):
        profile = Profile.objects.filter(user=request.user.id)
        if not profile.exists():
            return does_not_exists_response('Profile')
        # partial is True for PATCH request
        serializer = self.get_serializer(
            profile.get(),
            data=request.data,
            partial=True
        )
        if not serializer.is_valid():
            return invalid_serializer_response(serializer)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
