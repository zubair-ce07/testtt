from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.forms.models import model_to_dict

from ..models import User
from .serliazers import UserSerializer
from .permissions import isSameUser
from freelancing.utils.api.response import \
    invalid_serializer_response, missing_attribute_response


class UserApi(generics.ListCreateAPIView):
    """Rest api for users"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminUser, )


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

    def post(self, request, format=None):
        role = request.data.get('role')
        if not role:
            return missing_attribute_response('role')
        if role == "seller":
            updated_user = User.objects.filter(
                id=request.user.id
            ).update(is_buyer=False, is_seller=True)
        if role == "buyer":
            updated_user = User.objects.filter(
                id=request.user.id
            ).update(is_buyer=False, is_seller=True)

        print(request.user)
