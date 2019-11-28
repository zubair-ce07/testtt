from rest_framework.response import Response

from .serializers import (
    EducationSerializer,
    ExperienceSerializer,
    ProfileSerializer,
    SkillSerializer,
    UserSerializer
)
from .models import (
    Education,
    Experience,
    Profile,
    Skill,
    User
)
from rest_framework import viewsets
from rest_framework.decorators import action


class EducationView(viewsets.ModelViewSet):
    serializer_class = EducationSerializer
    queryset = Education.objects.all()


class ExperienceView(viewsets.ModelViewSet):
    serializer_class = ExperienceSerializer
    queryset = Experience.objects.all()


class SkillView(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(methods=['get'], detail=True)
    def education(self, request, pk=None):
        education = Education.objects.filter(user_id=pk).all()
        serializer_context = {
            'request': request,
        }
        education_json = EducationSerializer(education, context=serializer_context, many=True)
        return Response(education_json.data)

    @action(methods=['get'], detail=True)
    def experience(self, request, pk=None):
        experience_list = Experience.objects.filter(user_id=pk).all()
        serializer_context = {
            'request': request,
        }
        experience_list_json = ExperienceSerializer(experience_list, context=serializer_context, many=True)
        return Response(experience_list_json.data)

    @action(methods=['get'], detail=True)
    def skill(self, request, pk=None):
        skill_list = Skill.objects.filter(user_id=pk).all()
        serializer_context = {
            'request': request,
        }
        skill_list_json = SkillSerializer(skill_list, context=serializer_context, many=True)
        return Response(skill_list_json.data)


class ProfileView(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
