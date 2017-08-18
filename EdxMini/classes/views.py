from django.contrib.auth.models import User
from rest_framework import viewsets, permissions

from classes.models import Student, Course, Instructor, Enrollment
from classes.permissions import IsOwnerOrReadOnly
from classes.serializers import CourseSerializer, UserSerializer
from classes.serializers import EnrollmentSerializer
from classes.serializers import InstructorSerializer
from classes.serializers import StudentSerializer


# @api_view(['GET'])
# @permission_classes((permissions.AllowAny,))
# def api_root(request, format=None):
#     return Response({
#         'students': reverse('students-list', request=request, format=format),
#         'courses': reverse('courses-list', request=request, format=format),
#         'enrollments': reverse('enrollments-list', request=request, format=format),
#         'instructors': reverse('instructors-list', request=request, format=format),
#     })


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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
