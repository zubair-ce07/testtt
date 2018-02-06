from rest_framework.views import APIView
from api.Serializers.user_serializer import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import Group


class UserCreate(APIView):

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                new_group, created = Group.objects.get_or_create(
                    name=request.data['group'])
                user.groups.set([new_group])
                json = dict()
                json['result'] = "success"
                return Response(json, status=status.HTTP_201_CREATED)
        json = serializer.data
        json['result'] = 'failed'
        json['errors'] = serializer.errors
        return Response(json, status=status.HTTP_400_BAD_REQUEST)
