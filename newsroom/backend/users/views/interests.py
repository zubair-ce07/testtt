from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Q
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
        if request.user.is_authenticated:
            try:
                queryset = self.queryset.filter(user=request.user)
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data)
            except DatabaseError:
                Response(status=status.HTTP_400_BAD_REQUEST)
            except:
                Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        print(request);
        if request.user.is_authenticated:
            try:
                UserInterest.objects.filter(user=request.user).delete()

                queries = [Q(name=value) for value in request.data['interests']]
                query = queries.pop()
                for item in queries:
                    query |= item

                interests = Category.objects.filter(query)
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
        return Response(status=status.HTTP_401_UNAUTHORIZED)
