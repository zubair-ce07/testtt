from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authors.models import Author
from publishers.models import Publisher

from .serializers import AuthorSignupSerializer, PublisherSignupSerializer


class BaseSignUpView(generics.GenericAPIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            if user:
                data = serializer.data
                data['id'] = user.id
                token, _ = Token.objects.get_or_create(user=user)
                data['token'] = token.key
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                errors = "Invalid signup class"
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorSignup(BaseSignUpView):
    serializer_class = AuthorSignupSerializer


class PubliserSignup(BaseSignUpView):
    serializer_class = PublisherSignupSerializer


class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class LogIn(ObtainAuthToken):
    """Custom login view with extra userinfo"""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _created = Token.objects.get_or_create(user=user)

        user_data = {
            'token': token.key,
            "user_id": user.id,
            "username": user.username,
            "role": 'admin'
        }

        author = Author.objects.filter(pk=user.id).first()
        if author:
            user_data['name'] = author.get_full_name()
            user_data['role'] = 'author'
        else:
            publisher = Publisher.objects.filter(pk=user.id).first()
            if publisher:
                user_data['role'] = 'publisher'
                user_data['name'] = publisher.company_name

        return Response(user_data)
