# Create your views here.
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Program, Institution, Campus, Course, Semester
from .serializers import ProgramSerializer, InstitutionSerializer, CampusSerializer, CourseSerializer, \
    SemesterSerializer, LoginSerializer, RegisterSerializer


class InstitutionViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer


class CampusViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Campus.objects
    serializer_class = CampusSerializer

    def get_queryset(self):
        institution = self.kwargs['institution_id']
        return self.queryset.filter(institute=institution)


class ProgramViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Program.objects
    serializer_class = ProgramSerializer

    def get_queryset(self):
        institution = self.kwargs['institution_id']
        return self.queryset.filter(campus__institute=institution)


class CourseViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Course.objects
    serializer_class = CourseSerializer

    def get_queryset(self):
        program = self.kwargs['program_id']
        return self.queryset.filter(program=program).order_by('semester__number')


class SemesterViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Semester.objects
    serializer_class = SemesterSerializer

    def get_queryset(self):
        program = self.kwargs['program_id']
        return self.queryset.filter(program=program)


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=200)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        #  remove session
        return Response({'message': 'You have logged out'}, status=200)
