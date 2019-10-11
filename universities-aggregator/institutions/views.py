# Create your views here.
from rest_framework import viewsets

from .models import Program, Institution, Campus, Course
from .serializers import ProgramSerializer, InstitutionSerializer, CampusSerializer, CourseSerializer


class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer


class CampusViewSet(viewsets.ModelViewSet):
    queryset = Campus.objects
    serializer_class = CampusSerializer

    def get_queryset(self):
        institution = self.kwargs['institution_id']
        return self.queryset.filter(institute=institution)


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects
    serializer_class = ProgramSerializer

    def get_queryset(self):
        institution = self.kwargs['institution_id']
        return self.queryset.filter(campus__institute=institution)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects
    serializer_class = CourseSerializer

    def get_queryset(self):
        program = self.kwargs['program_id']
        return self.queryset.filter(program=program).order_by('semester__number')
