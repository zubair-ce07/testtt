from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework import generics, mixins, status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.core import serializers
from system.models import Appraisal, Competence
from system.serializer import UserSerializer, CompetenceSerializer


User = get_user_model()


#---------------------------------------User-Api

class UserRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = UserSerializer

    def get_queryset(self):
        qs = User.objects.all()
        if self.request._user.is_authenticated:
            if self.request._user.user_level != "admin":
                return qs.filter(report_to=self.request._user.pk)
            return qs


class UserAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = UserSerializer

    def get_queryset(self):
        qs = User.objects.all()
        if self.request._user.is_authenticated:
            if self.request._user.user_level != "admin":
                return qs.filter(report_to=self.request._user.pk)
            return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

#---------------------------------------Appraisal-API

class AppraisalAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    serializer_class = CompetenceSerializer

    def get_queryset(self):
        qs = Competence.objects.all()
        if self.request._user.is_authenticated:
            if self.request._user.user_level == "employee":
                return qs.filter(appraisal__to_user=self.request._user.pk)
            if self.request._user.user_level == "manager":
                return qs.filter(appraisal__from_user=self.request._user.pk)
            return qs

    def post(self, request, *args, **kwargs):
        serializer = CompetenceSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

class AppraisalRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = CompetenceSerializer

    def get_queryset(self):
        qs = Competence.objects.all()
        if self.request._user.is_authenticated:
            if self.request._user.user_level == "employee":
                return qs.filter(appraisal__to_user=self.request._user.pk)
            if self.request._user.user_level == "manager":
                return qs.filter(appraisal__from_user=self.request._user.pk)
            return qs

    def get_object(self):
        pk = self.kwargs.get("pk")
        try:
            appraisal = Appraisal.objects.get(pk=pk)
            return appraisal.competence_set.all()[0]
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Object does not exist.")

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.appraisal.delete()
