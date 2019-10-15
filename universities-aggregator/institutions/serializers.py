from .models import Program, Campus, Institution, Course, Semester

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


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'

    semester_courses = CourseSerializer(read_only=True, many=True)
