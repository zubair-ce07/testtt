from django.db import DatabaseError
from django.core.validators import validate_email
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from backend.users.models import User


class UserCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            email = request.data['email']
            password = request.data['password']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            validate_email(email)
            user = User(username=email, email=email, first_name=first_name, last_name=last_name)
            user.set_password(password)
            user.save()
            return Response(request.data, status=status.HTTP_200_OK)
        except validate_email.ValidationError:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except KeyError:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except DatabaseError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
