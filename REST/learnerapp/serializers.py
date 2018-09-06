import datetime

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import IntegrityError
from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers

from learnerapp import models, constants, validators


class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.CharField(source='get_user_type_display', read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True, validators=[validators.email_validation])

    class Meta:
        model = models.CustomUser
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'user_type')
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'validators': [UnicodeUsernameValidator], }, }


class UserUpdateSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ('username', 'email', 'first_name', 'last_name', 'user_type', )
        extra_kwargs = {
            'username': {'read_only': True, }, }


class InstructorSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    details = serializers.HyperlinkedIdentityField(view_name='instructor-detail', format='html')

    class Meta:
        model = models.Instructor
        fields = ('details', 'user', 'institute', 'designation')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['user_type'] = constants.TEACHER
        password = user_data.pop('password')

        try:
            user = models.CustomUser.objects.create(**user_data)
            user.set_password(password)
            user.save()
            instructor = models.Instructor.objects.create(user=user, **validated_data)
            return instructor
        except IntegrityError:
            raise serializers.ValidationError("The Username Already exists")


class InstructorUpdateSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()

    class Meta:
        model = models.Instructor
        fields = ('user', 'institute', 'designation')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        username = instance.user.username
        models.CustomUser.objects.filter(username=username).update(**user_data)
        return super(InstructorUpdateSerializer, self).update(instance, validated_data)


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    details = serializers.HyperlinkedIdentityField(view_name='student-detail', format='html')

    class Meta:
        model = models.Student
        fields = ('details', 'user', 'dob', 'university')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['user_type'] = constants.STUDENT
        password = user_data.pop('password')

        try:
            user = models.CustomUser.objects.create(**user_data)
            user.set_password(password)
            user.save()
            student = models.Student.objects.create(user=user, **validated_data)
            return student
        except IntegrityError:
            raise serializers.ValidationError("The Username Already exists")


class StudentUpdateSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()

    class Meta:
        model = models.Student
        fields = ('user', 'dob', 'university')
        extra_kwargs = {
            'dob': {'validators': [validators.dob_validation], }, }

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        username = instance.user.username
        models.CustomUser.objects.filter(username=username).update(**user_data)
        return super(StudentUpdateSerializer, self).update(instance, validated_data)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = '__all__'

    def to_representation(self, instance):
        instance = super(CourseSerializer, self).to_representation(instance)
        instructor_info = []
        for pk in instance['instructors']:
            instructor = models.Instructor.objects.get(pk=pk)
            instructor_info.append((instructor.user.first_name,
                                    instructor.designation + "-" + instructor.institute))
        instance['instructors'] = instructor_info
        return instance

    def validate(self, data):
        start_date = data['start_date']
        end_date = data['end_date']
        today = datetime.datetime.now().date()
        if start_date > end_date:
            raise serializers.ValidationError('End Date cannot be prior to Start date')
        if start_date < today:
            raise serializers.ValidationError('Start date cannot be prior to today ')
        return data


class ActiveCourseRelatedField(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        current_user = self.context['request'].user
        if current_user.is_authenticated():
            enrollments = models.Enrollment.objects.filter(student__user=current_user)
            ids = [value[0] for value in list(enrollments.values_list('course__id'))]
            return self.queryset.filter(Q(status__in=[constants.ACTIVE]),
                                        ~Q(id__in=ids))


class EnrollmentSerializer(serializers.ModelSerializer):
    unenroll = serializers.HyperlinkedIdentityField(view_name='unenroll', format='html')

    class Meta:
        model = models.Enrollment
        fields = ('unenroll', 'date_joined', 'student', 'course',)
        extra_kwargs = {
            'unenroll': {'read_only': True},
            'date_joined': {'read_only': True}}

    def create(self, validated_data):
        validated_data['date_joined'] = str(timezone.now())
        instance = models.Enrollment.objects.create(**validated_data)
        return instance

    def to_representation(self, instance):
        instance = super(EnrollmentSerializer, self).to_representation(instance)
        student = models.Student.objects.get(pk=instance['student'])
        course = models.Course.objects.get(pk=instance['course'])
        instance['student'] = student.user.first_name
        instance['course'] = course.title
        return instance


class StudentEnrollment(EnrollmentSerializer):
    course = ActiveCourseRelatedField(queryset=models.Course.objects.all())

    class Meta:
        model = models.Enrollment
        fields = ('unenroll', 'date_joined', 'student', 'course',)
        extra_kwargs = {
            'student': {'read_only': True},
            'unenroll': {'read_only': True},
            'date_joined': {'read_only': True}}

    def create(self, validated_data):
        student = models.Student.objects.get(user=self.context['request'].user)
        validated_data['student'] = student
        validated_data['date_joined'] = str(timezone.now())
        instance = models.Enrollment.objects.create(**validated_data)
        return instance