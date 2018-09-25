
from django.http import Http404
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework import generics, mixins, status, serializers
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from system.models import Appraisal, Competence
from system.serializer import UserSerializer, CompetenceSerializer


User = get_user_model()


class AppraisalAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'
    serializer_class = AppraisalSerializer

    def get(self, request, format=None, pk=None):
        if pk is None:
            serializer =  AppraisalSerializer(self.get_queryset(), many=True)
            return Response(serializer.data)
        else:
            appraisal = self.get_object(pk)
            serializer =  AppraisalSerializer(appraisal)
            return Response(serializer.data)

    def post(self, request, format=None, pk=None):
        serializer =  AppraisalSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=ValueError):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        appraisal = self.get_object(pk)
        serializer =  AppraisalSerializer(appraisal, data=request.data,
                                          context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        appraisal = self.get_object(pk)
        appraisal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        qs = Appraisal.objects.all()
        if self.request.user.user_level == "employee":
            return qs.filter(to_user=self.request.user.pk)
        if self.request.user.user_level == "manager":
            return qs.filter(from_user=self.request.user.pk)
        return qs

    def get_object(self, pk):
        try:
            appraisal = Appraisal.objects.get(pk=pk)
            return appraisal
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Object does not exist.")

class UserAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'
    serializer_class = UserSerializer

    def get(self, request, format=None, pk=None):
        if pk is None:
            serializer = UserSerializer(self.get_queryset(), many=True)
            return Response(serializer.data)
        else:
            user = self.get_object(pk)
            serializer = UserSerializer(user)
            return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data,
                                    context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None, pk=None):
        serializer = UserSerializer(data=request.data,
                                    context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get_queryset(self):
        qs = User.objects.all()
        if self.request._user.user_level != "admin":
            return qs.filter(report_to=self.request._user.pk)
        return qs

class SignupAPI(APIView):
    serializer_class = SignUpSerializer

    def post(self, request, format=None, pk=None):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
