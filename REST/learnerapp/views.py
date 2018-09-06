from rest_framework import filters, generics, viewsets, permissions

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
        if self.request.user.user_type == constants.TEACHER:
            return models.Student.objects.all()
        return models.Student.objects.filter(user__id=self.request.user.id)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          custom_permissions.InstructorOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['title']


class EnrollmentView(viewsets.ViewSetMixin, generics.ListCreateAPIView):
    serializer_class = serializers.EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    action_serializers = {
        'student': serializers.StudentEnrollment,
    }

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        if self.request.user.is_authenticated():
            if self.request.user.user_type == constants.TEACHER:
                return models.Enrollment.objects.all()
            return models.Enrollment.objects.filter(student__user_id=self.request.user.id)

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            user_type = self.request.user.get_user_type_display()
            if user_type in self.action_serializers:
                return self.action_serializers[user_type]
        return super(EnrollmentView, self).get_serializer_class()


class UnenrollView(generics.RetrieveDestroyAPIView):
    queryset = models.Enrollment.objects.all()
    serializer_class = serializers.EnrollmentSerializer
