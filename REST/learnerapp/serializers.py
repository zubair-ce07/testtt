import datetime

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import IntegrityError
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

    def validate(self, data):
        start_date = data['start_date']
        end_date = data['end_date']
        today = datetime.datetime.now().date()
        if start_date > end_date:
            raise serializers.ValidationError('End Date cannot be prior to Start date')
        if start_date < today:
            raise serializers.ValidationError('Start date cannot be prior to today ')
        return data
