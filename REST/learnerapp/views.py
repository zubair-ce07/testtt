from rest_framework import viewsets, permissions, filters

from learnerapp import constants, models, serializers
from learnerapp import permissions as custom_permissions


class InstructorViewSet(viewsets.ModelViewSet):
    queryset = models.Instructor.objects.all()
    serializer_class = serializers.InstructorSerializer
    permission_classes = (custom_permissions.InstructorAddPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['user__username']
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
    filter_backends = (filters.SearchFilter,)
    search_fields = ['user__username']


    action_serializers = {
        'update': serializers.StudentUpdateSerializer,
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super(StudentViewSet, self).get_serializer_class()

    def get_queryset(self):
        if self.request.user.user_type == constants.TEACHER or 1:
            return models.Student.objects.all()
        return models.Student.objects.filter(user__id=self.request.user.id)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          custom_permissions.InstructorOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['title']
