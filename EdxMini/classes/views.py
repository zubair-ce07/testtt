from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.decorators import detail_route
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response

from classes.models import Student, Course, Instructor, Enrollment
from classes.permissions import IsOwnerOrReadOnly
from classes.serializers import CourseSerializer, UserSerializer, EnrollmentUpdateSerializer
from classes.serializers import EnrollmentSerializer
from classes.serializers import InstructorSerializer
from classes.serializers import StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class InstructorViewSet(viewsets.ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = (DjangoModelPermissions,)

    def get_queryset(self):
        queryset = Enrollment.objects.all()
        status = self.request.query_params.get('status', None)
        if status is not None:
            queryset = queryset.filter(status=status)
        return queryset

    @detail_route(methods=['get'])
    def students(self, request, pk):
        student_list = get_students_by_course_id(pk)
        return Response(student_list)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        self.serializer_class = EnrollmentUpdateSerializer
        return super(EnrollmentViewSet, self).update(request, *args, **kwargs)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def get_students_by_course_id(course_id):
    enrollments = Enrollment.objects.filter(course=course_id)
    student_list = Student.objects.filter(id__in=enrollments.values('student_id'))
    return StudentSerializer(student_list, many=True).data
