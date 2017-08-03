from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Q
from backend.users.serializers.interest import UserInterestSerializer
from backend.users.models import UserInterest
from backend.categories.models import Category


class UserInterestViewSet(APIView):
    queryset = UserInterest.objects.all()
    serializer_class = UserInterestSerializer

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            queryset = self.queryset.filter(user=request.user)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request_data = dict(request.data.lists())

            UserInterest.objects.filter(user=request.user).delete()

            queries = [Q(name=value) for value in request_data['interests']]
            query = queries.pop()
            for item in queries:
                query |= item

            interests = Category.objects.filter(query)

            UserInterest.objects.bulk_create([UserInterest(user=request.user,
                                                           category=interest) for interest in interests])

            return Response(request.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
