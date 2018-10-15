"""
Contains the serializers for API.
"""
from rest_framework import serializers
from rest_framework.exceptions import APIException
from django.contrib.auth.models import User

from accounts.models import UserProfile
from .models import Saloon, Feedback, Appointment, Area, City, Country
from .constants import PROCESS_APPOINTMENT_OWNER_STATUS_CHOICES
from saloon_api.settings import MEDIA_URL


class UserSerializer(serializers.ModelSerializer):
    # password should not be visible so make it write only
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    user_type = serializers.CharField(read_only=True, source='profile__user_type')

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'user_type')


class SaloonSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(read_only=True)
    country = serializers.CharField(read_only=True)
    area = serializers.CharField(max_length=30)

    class Meta:
        model = Saloon
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class SaloonSearchSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    country = CountrySerializer()
    area = AreaSerializer()

    class Meta:
        model = Saloon
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user__username')
    email = serializers.CharField(source='user__email')
    first_name = serializers.CharField(source='user__first_name')
    last_name = serializers.CharField(source='user__last_name')
    saloon = serializers.IntegerField(read_only=True)
    pk = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserProfile
        depth = 1
        fields = ('pk', 'username', 'email', 'first_name', 'last_name', 'birth_date',
                  'contact_number', 'address', 'saloon')


class FeedbackSerializer(serializers.ModelSerializer):
    saloon = serializers.CharField(read_only=True, source='saloon__id')
    user = serializers.CharField(read_only=True, source='user__id')

    class Meta:
        model = Feedback
        depth = 1
        fields = ('id', 'saloon', 'rate', 'description', 'user')


class RequestAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('description',)


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'


class ProcessAppointmentSerializer(serializers.ModelSerializer):
    # to show the booked_slot in read only field add SerializerMethodField
    booked_slots = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ('customer', 'attender', 'saloon', 'time', 'status', 'duration', 'booked_slots')
        read_only_fields = ('saloon', 'customer')

    def __init__(self, *args, **kwargs):
        """
        Initializes attributes and changes the fields.
        """
        super(ProcessAppointmentSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        appointment_saloon = self.context.get("appointment_saloon")
        try:
            if appointment_saloon is None:
                # Means record doesn't exist
                saloon_id = -1
            else:
                saloon_id = appointment_saloon.id
            saloon = Saloon.objects.get(owner=request.user, id=saloon_id)
        except Saloon.DoesNotExist:
            raise APIException('Saloon does not exist !!!')
        queryset = User.objects.filter(profile__user_type='e', profile__saloon=saloon)

        if not queryset.exists():
            raise APIException('You don\'t have any employee to assign !!!')
        # attenders available in the saloon
        self.fields['attender'] = serializers.PrimaryKeyRelatedField(queryset=queryset)
        self.fields['status'] = serializers.ChoiceField(choices=PROCESS_APPOINTMENT_OWNER_STATUS_CHOICES)

    def get_booked_slots(self, obj):
        return self.context.get('booked_slots')

    def validate(self, attrs):
        """
        Does some extra validation like if status of appointment is accepted then owner
        should must set the time and attender to the appointment.
        And the minimum duration should be 5 (minutes).
        """
        if attrs['status'] == 'accepted':
            if attrs['time'] is None:
                raise serializers.ValidationError('You didn\'t enter the time !!!')
            if attrs['attender'] is None:
                raise serializers.ValidationError('You didn\'t enter the attender !!!')
            if attrs['duration'] is None or attrs['duration'] < 5:
                raise serializers.ValidationError('You didn\'t enter the valid duration (more than 4) !!!')
        return super().validate(attrs)


class UserProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(max_length=None, use_url=True, write_only=True, allow_null=True)
    username = serializers.CharField(source='user__username')
    first_name = serializers.CharField(source='user__first_name')
    last_name = serializers.CharField(source='user__last_name')
    email = serializers.EmailField(source='user__email')

    profile_picture_url = serializers.SerializerMethodField()

    def get_profile_picture_url(self, obj):
        """
        Generates absolute URL of the profile picture.
        """
        request = self.context['request']
        return request.build_absolute_uri(MEDIA_URL + obj['profile_picture'])

    class Meta:
        model = UserProfile
        depth = 1
        fields = (
            'username', 'first_name', 'last_name', 'email', 'contact_number', 'birth_date', 'user_type',
            'address', 'profile_picture', 'profile_picture_url',
        )
        # fields = '__all__'
        read_only_fields = ('user_type',)
