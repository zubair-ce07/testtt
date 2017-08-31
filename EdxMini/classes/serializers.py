from django.contrib.auth.models import User
from rest_framework import serializers

from classes import views as class_views
from classes.models import Student, Instructor, Course, Enrollment


class EnrollmentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    url = serializers.HyperlinkedIdentityField(view_name='enrollment-detail')
    course = serializers.StringRelatedField()
    student = serializers.StringRelatedField()

    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ('updated_at', 'created_at')


class EnrollmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['status']


class CourseSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    url = serializers.HyperlinkedIdentityField(view_name='course-detail')
    students = serializers.SerializerMethodField()
    instructors = serializers.StringRelatedField(many=True)

    def get_students(self, obj):
        student_list = class_views.get_students_by_course_id(obj.id)
        return student_list

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('updated_at', 'created_at')


class InstructorSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    url = serializers.HyperlinkedIdentityField(view_name='instructor-detail')
    fullname = serializers.SerializerMethodField()

    def get_fullname(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)

    class Meta:
        model = Instructor
        fields = '__all__'
        read_only_fields = ('updated_at', 'created_at')


class StudentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    fullname = serializers.SerializerMethodField()

    def get_fullname(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)

    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ('updated_at', 'created_at')


class UserSerializer(serializers.ModelSerializer):
    student = serializers.HyperlinkedIdentityField(many=True, view_name='student-detail', read_only=True)
    course = serializers.HyperlinkedIdentityField(many=True, view_name='course-detail', read_only=True)
    instructor = serializers.HyperlinkedIdentityField(many=True, view_name='instructor-detail', read_only=True)
    enrollment = serializers.HyperlinkedIdentityField(many=True, view_name='enrollment-detail', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'student', 'course', 'enrollment', 'instructor')
