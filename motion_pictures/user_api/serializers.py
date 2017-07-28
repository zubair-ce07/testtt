from rest_framework import serializers
from user_api.models import User, Address, Profile, Designation


class AddressSerializer(serializers.ModelSerializer):
    """
    serializes data for address model
    """
    class Meta:
        model = Address
        fields = ('street', 'city',)

    @classmethod
    def update(cls, instance, validated_data):
        instance.street = validated_data.get('street', instance.street)
        instance.city = validated_data.get('city', instance.city)
        instance.save()
        return instance


class DesignationSerializer(serializers.ModelSerializer):
    """
        serializes data for designation model
        """
    job_title = serializers.CharField()

    class Meta:
        model = Designation
        fields = ('job_title',)

    @classmethod
    def update(cls, instance, validated_data):
        try:
            job_title = validated_data.pop('job_title')
            instance = Designation.get_or_create(job_title)
        except KeyError:
            pass

        return instance


class ProfileSerializer(serializers.ModelSerializer):
    """
        serializes data for profile model
        """
    address = AddressSerializer()
    designation = DesignationSerializer()

    class Meta:
        model = Profile
        fields = ('gender', 'phone', 'designation', 'address',)

    @classmethod
    def update(cls, instance, validated_data):
        instance.gender = validated_data.get('gender', instance.gender)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.designation = DesignationSerializer.update(instance.designation, validated_data.get('designation', {}))
        AddressSerializer.update(instance.address, validated_data.get('address', {}))
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    """
        serializes data for user model
        """
    profile = ProfileSerializer()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'profile', 'password',)

    def create(self, validated_data):
        profile = validated_data.pop('profile')
        address = profile.pop('address')
        designation = profile.pop('designation')

        user = User.objects.create_user(**validated_data)
        address = Address.objects.create(**address)
        designation = Designation.get_or_create(**designation)
        profile = Profile.objects.create(user=user, address=address, designation=designation, **profile)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    serializes data for User model when request for
    updating user. it excludes email and password
    """
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'profile',)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        ProfileSerializer.update(instance.profile, validated_data.get('profile', {}))
        return instance


class AuthTokenSerializer(serializers.Serializer):
    """
    serializes email and password for getting auth token
    """
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})
