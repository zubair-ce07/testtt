import json

from django.contrib.auth import authenticate, login
from rest_framework import status, views
from rest_framework.response import Response

from web.users.serializers.profile_serializer import ProfileSerializer


class LoginView(views.APIView):

    # noinspection PyMethodMayBeStatic
    def post(self, request, format=None):

        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email', None)
        password = data.get('password', None)

        account = authenticate(email=email, password=password)

        if account is not None:
            if account.is_active:
                login(request, account)
                serialized = ProfileSerializer(account)
                response = Response(serialized.data)
            else:
                response = Response({
                                'status': 'Unauthorized',
                                'message': 'This account has been disabled.'
                                },  status=status.HTTP_401_UNAUTHORIZED)
        else:
            response = Response({
                            'status': 'Unauthorized',
                            'message': 'Username/password is invalid.'
                            }, status=status.HTTP_401_UNAUTHORIZED)

        return response