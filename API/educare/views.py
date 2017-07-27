from __future__ import unicode_literals
from educare.serializers import (
    UserLoginSerializer,
    ResetPasswordSerializer,
    TutorProfileSerializer,
    StudentSerializer,
    TutorSerializer,
    StudentProfileSerializer,
    )
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import (
    RetrieveUpdateAPIView,
    RetrieveAPIView,
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    )
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Student, Tutor
from .permissions import IsOwner, IsStudent, IsTutor


class UserView(APIView):

    def user_is_student(self):
        username = self.kwargs["username"]
        user = User.objects.filter(username=username)
        if user.exists():
            user_object = user.first()
            return user_object.user_type == 'S'

    def get_queryset(self):
        username = self.kwargs["username"]
        if self.user_is_student():
            return Student.objects.filter(username=username)
        return Tutor.objects.filter(username=username)

    def get_serializer_class(self):
        if self.user_is_student():
            return StudentProfileSerializer
        return TutorProfileSerializer

    def get_object(self):
        username = self.kwargs["username"]
        if self.user_is_student():
            student_object = get_object_or_404(Student, username=username)
            self.check_object_permissions(self.request, student_object)
            return student_object
        tutor_object = get_object_or_404(Tutor, username=username)
        self.check_object_permissions(self.request, tutor_object)
        return tutor_object


class StudentSignUpView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = StudentSerializer
    queryset = Student.objects.all()


class TutorSignUpView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = TutorSerializer
    queryset = Tutor.objects.all()


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = {'username': serializer.data.get('username')}
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserProfileChangeAPIView(UserView, RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwner, permissions.IsAuthenticated)
    parser_classes = (MultiPartParser, FormParser,)


class ResetPasswordView(RetrieveUpdateAPIView):
    permission_classes = (IsOwner, permissions.IsAuthenticated)
    serializer_class = ResetPasswordSerializer

    def get_object(self, queryset=None):
        username = self.kwargs["username"]
        user_object = User.objects.filter(username=username)
        self.check_object_permissions(self.request, user_object.first())
        return user_object.first()

    def put(self, request, *args, **kwargs):
        user_object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not user_object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=HTTP_400_BAD_REQUEST)
            user_object.set_password(serializer.data.get("new_password"))
            user_object.save()
            return Response("Success.", status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserProfileView(UserView, RetrieveAPIView):
    lookup_field = 'username'


class TutorListView(ListAPIView):
    permission_classes = (IsStudent, permissions.IsAuthenticated,)
    serializer_class = TutorProfileSerializer
    queryset = Tutor.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('location', )


class StudentListView(ListAPIView):
    permission_classes = (permissions.IsAuthenticated, IsTutor)
    serializer_class = StudentProfileSerializer
    queryset = Student.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('grade', )
