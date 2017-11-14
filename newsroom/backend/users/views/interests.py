from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db import DatabaseError
from backend.users.serializers.interest import UserInterestSerializer
from backend.users.models import UserInterest
from backend.categories.models import Category
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class UserInterestAPIView(APIView):
    queryset = UserInterest.objects.all()
    serializer_class = UserInterestSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.queryset.filter(user=request.user)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        except DatabaseError:
            Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        try:
            UserInterest.objects.filter(user=request.user).delete()

            interests = Category.objects.filter(name__in=request.data["interests"])
            UserInterest.objects.bulk_create([UserInterest(user=request.user,
                                                           category=interest) for interest in interests])

            queryset = self.queryset.filter(user=request.user)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except DatabaseError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
