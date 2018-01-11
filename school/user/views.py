from django.contrib.auth.models import Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.serializers import UserSerializer, UserListSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


class UserList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, group_id=False, format=None):
        
        if (group_id):
            users = User.objects.filter(groups__id=group_id)
        else:
            users = User.objects.all()
        
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format='json'):
        user_data = UserSerializer(data=request.data)
        if user_data.is_valid():
            user = user_data.save()
            if 'first_name' in user_data or 'last_name' in user_data:

                if 'first_name' in user_data:
                    user.first_name = user_data['first_name'].value
                
                if 'last_name' in user_data:
                    user.last_name = user_data['last_name'].value
                
                user.save()
            
            if request.POST.get('group_id') is not None:
                group = Group.objects.get(id=request.POST.get('group_id'))
                user.groups.add(group)
            
            if user:
                token = Token.objects.create(user=user)
                json = user_data.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(user_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    
    permission_classes = (IsAuthenticated,)

    def get_object(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise Http404
            
    def get(self, request, user_id, format=None):
        user = self.get_object(user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, user_id, format=None):
        user_data = self.get_object(user_id)
        serializer = UserSerializer(user_data, data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            if request.POST.get('group_id') is not None:
                user.groups.clear()
                group = Group.objects.get(id=request.POST.get('group_id'))
                user.groups.add(group)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
