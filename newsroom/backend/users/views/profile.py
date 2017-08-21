from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import DatabaseError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from backend.users.serializers.user import UserSerializer
from backend.users.models import User
from rest_framework.authtoken.models import Token


class UserProfileAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.queryset.get(id=request.user.id)
            serializer = self.serializer_class(queryset)
            return Response(serializer.data)
        except DatabaseError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_402_PAYMENT_REQUIRED)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                User.objects.update_or_create(email=request.user.email,
                                              defaults=request.data)
                return Response(request.data, status=status.HTTP_200_OK)
            except KeyError:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            except DatabaseError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

for user in User.objects.all():
    Token.objects.get_or_create(user=user)