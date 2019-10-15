from .models import Program, Campus, Institution, Course

from rest_framework import serializers


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'


class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = '__all__'


class ProgramSerializer(serializers.ModelSerializer):
    campus = CampusSerializer(read_only=True)
    category = serializers.CharField(source='get_category_display')

    class Meta:
        model = Program
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
