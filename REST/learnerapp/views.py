from learnerapp import models, serializers
from rest_framework import viewsets, permissions

from learnerapp import permissions as custom_permissions


class InstructorViewSet(viewsets.ModelViewSet):
    queryset = models.Instructor.objects.all()
    serializer_class = serializers.InstructorSerializer
    permission_classes = (custom_permissions.UserOnlyUpdatePermission,)

    action_serializers = {
        'update': serializers.InstructorUpdateSerializer,
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super(InstructorViewSet, self).get_serializer_class()


class StudentViewSet(viewsets.ModelViewSet):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    permission_classes = (custom_permissions.UserOnlyUpdatePermission,)

    action_serializers = {
        'update': serializers.StudentUpdateSerializer,
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super(StudentViewSet, self).get_serializer_class()


class CourseViewSet(viewsets.ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
