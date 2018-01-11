from rest_framework import generics
from course.models import Course
from course.serializers import CourseSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class CourseList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_url_kwarg = 'course_id'
    
