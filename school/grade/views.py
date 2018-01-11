from rest_framework import generics
from grade.models import Grade, GradeCourse, GradeTeacher, GradeStudent
from grade.serializers import GradeSerializer, GradeCourseSerializer, GradeTeacherSerializer, GradeStudentSerializer, GradeListSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class GradeList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Grade.objects.all()
    serializer_class = GradeListSerializer
    

class GradeDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    lookup_url_kwarg = 'grade_id'

# Grade Course

class GradeCourseList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = GradeCourse.objects.all()
    serializer_class = GradeCourseSerializer
    
class GradeCourseDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = GradeCourse.objects.all()
    serializer_class = GradeCourseSerializer
    lookup_url_kwarg = 'gradecourse_id'

# Grade Students

class GradeStudentList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = GradeStudent.objects.all()
    serializer_class = GradeStudentSerializer
    
class GradeStudentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = GradeStudent.objects.all()
    serializer_class = GradeStudentSerializer
    lookup_url_kwarg = 'gradestudent_id'

# Grade Teachers

class GradeTeacherList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = GradeTeacher.objects.all()
    serializer_class = GradeTeacherSerializer
    
class GradeTeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = GradeTeacher.objects.all()
    serializer_class = GradeTeacherSerializer
    lookup_url_kwarg = 'gradeteacher_id'
