from django.contrib.auth.models import User
from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse

from classes.models import Student, Course, Instructor, Enrollment
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


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class InstructorViewSet(viewsets.ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer