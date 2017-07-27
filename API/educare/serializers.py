from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import User, Tutor, Student
from django.db.models import Q


class UserSerializer(serializers.ModelSerializer):
    subjects = serializers.MultipleChoiceField(choices=User.SUBJECTS_CHOICES)

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'birth_date',
            'location',
            'gender',
            'subjects',
            'biography',
            'profile_picture',
        )

    @staticmethod
    def set_user_attributes(user_object, validated_data, is_student):
        user_object.email = validated_data['email']
        user_object.first_name = validated_data['first_name']
        user_object.last_name = validated_data['last_name']
        user_object.birth_date = validated_data['birth_date']
        user_object.gender = validated_data['gender']
        user_object.location = validated_data['location']
        user_object.biography = validated_data['biography']
        user_object.subjects = list(validated_data['subjects'])
        if is_student:
            user_object.user_type = 'S'
            user_object.grade = validated_data['grade']
        else:
            user_object.user_type = 'T'
            user_object.education = validated_data['education']
            user_object.phone_number = validated_data['phone_number']
        user_object.save()
        return user_object


class StudentSerializer(UserSerializer):
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta(UserSerializer.Meta):
        model = Student
        fields = UserSerializer.Meta.fields + ('username', 'password', 'grade', 'subjects', )

    def create(self, validated_data):
        student = Student.objects.create_user(validated_data['username'], validated_data['password'])
        return self.set_user_attributes(student, validated_data, True)


class TutorSerializer(UserSerializer):
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta(UserSerializer.Meta):
        model = Tutor
        fields = UserSerializer.Meta.fields + ('username', 'password', 'education', 'subjects', 'phone_number',)

    def create(self, validated_data):
        tutor = Tutor.objects.create_user(validated_data['username'], validated_data['password'])
        return self.set_user_attributes(tutor, validated_data, False)


class UserLoginSerializer(serializers.ModelSerializer):
    token = serializers.CharField(allow_blank=True, read_only=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username','password', 'token',)
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        user_object = None
        username = data.get('username')
        password = data.get('password')
        user = User.objects.filter(Q(username=username))
        if user.exists():
            user_object = user.first()
        else:
            raise ValidationError('This username is invalid')
        if user_object:
            if not user_object.check_password(password):
                raise ValidationError('Incorrect Credentials! Please Try Again')
        return data


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField( style={'input_type': 'password'}, default='')
    new_password = serializers.CharField( style={'input_type': 'password'}, default='')


class StudentProfileSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = Student
        fields = ('username', 'grade', 'subjects',) + UserSerializer.Meta.fields

    def update(self, instance, validated_data):
        return self.set_user_attributes(instance, validated_data, True)


class TutorProfileSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = Tutor
        fields = ('username', 'subjects', 'education', 'phone_number', ) + UserSerializer.Meta.fields

    def update(self, instance, validated_data):
        return self.set_user_attributes(instance, validated_data, False)
