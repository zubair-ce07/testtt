from rest_framework import serializers
from user_api.models import User, Address, Profile, Designation


class AddressSerializer(serializers.ModelSerializer):
    """
    serializes data for address model
    """
    class Meta:
        model = Address
        fields = ('street', 'city', 'country', 'zip_code')


class DesignationSerializer(serializers.ModelSerializer):
    """
    serializes data for designation model
    """
    class Meta:
        model = Designation
        fields = ('job_title',)
        extra_kwargs = {
            'job_title': {'validators': []},
        }


class ProfileSerializer(serializers.ModelSerializer):
    """
    serializes data for profile model
    """
    address = serializers.SerializerMethodField()
    designation = DesignationSerializer()

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'gender', 'designation', 'address',)

    def get_address(self, profile):
        address = getattr(profile, 'address', False)
        return AddressSerializer(address).data if address else None

    def create(self, validated_data):
        designation = Designation.objects.get(**validated_data.pop('designation'))

        profile = Profile.objects.create(
            user=validated_data.pop('user'),
            address=validated_data.pop('address'),
            designation=designation,
            **validated_data
        )

        return profile

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.gender = validated_data.get('gender', instance.gender)

        # if designation is in update request data then sets with that instance
        try:
            instance.designation = Designation.objects.get(**validated_data['designation'])
        except (KeyError, Designation.DoesNotExist):
            # data not in request provided or designation not in db
            pass
        instance.address = validated_data.pop('address')
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    """
    serializes data for user model. Along with user details provides
    with user's own token.
    """
    profile = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'phone', 'email', 'profile', 'password', 'token',)

    def get_profile(self, user):
        profile = getattr(user, 'profile', False)
        return ProfileSerializer(profile).data if profile else None

    def get_token(self, user):
        """
        Checks if requesting user is same as serializing object
        and if are same returns key of token

        Arguments:
            user (User): user being serialized

        Returns:
            token_key (str): key of token associated to user
        """
        return None if user != self.context['request'].user else user.auth_token.key

    def create(self, validated_data):
        serializer = AddressSerializer(data=self.initial_data.get('profile', {}).get('address', {}))
        serializer.is_valid(raise_exception=True)
        address = serializer.save()

        serializer = ProfileSerializer(data=self.initial_data.get('profile', {}))
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(**validated_data)
        serializer.save(user=user, address=address)
        return user

    def update(self, instance, validated_data):
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        # saving changes to profile model for the user
        profile = getattr(instance, 'profile', None)
        address = getattr(instance.profile, 'address', None) if profile else None

        address_serializer = AddressSerializer(
            address,
            self.initial_data.get('profile', {}).get('address', {}),
            partial=self.partial
        )
        address_serializer.is_valid(raise_exception=True)
        address = address_serializer.save()

        profile_serializer = ProfileSerializer(
            profile,
            self.initial_data.get('profile', {}),
            partial=self.partial
        )
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save(user=instance, address=address)

        instance.save()
        return instance
