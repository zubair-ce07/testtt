from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from backend.users.serializers.user import UserSerializer


class UserCreateAPIView(APIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)