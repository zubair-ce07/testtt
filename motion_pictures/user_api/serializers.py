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
    address = AddressSerializer()
    designation = DesignationSerializer()

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'gender', 'designation', 'address',)

    def create(self, validated_data):
        address = AddressSerializer(data=validated_data.pop('address'))
        address.is_valid(raise_exception=True)
        address.save()

        designation, created = Designation.objects.get_or_create(**validated_data.pop('designation'))

        profile = Profile.objects.create(
            user=validated_data.pop('user'),
            address=address,
            designation=designation,
            **validated_data
        )

        return profile

    def update(self, instance, validated_data):
        # if designation is in update request data then sets with new instance
        try:
            job_title = validated_data.pop('designation').pop('job_title')
            instance.designation, created = Designation.objects.get_or_create(job_title=job_title)
        except KeyError:
            pass

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.save()

        # saving updates in address
        try:
            address = instance.address
        except Address.DoesNotExist:
            address = None

        serializer = AddressSerializer(address, validated_data.get('address', {}), partial=self.partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return instance


class UserSerializer(serializers.ModelSerializer):
    """
    serializes data for user model. Along with user details provides
    with user's own token.
    """
    profile = ProfileSerializer()
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'phone', 'email', 'profile', 'password', 'token',)

    def get_token(self, obj):
        """
        Checks if requesting user is same as serializing object
        and if are same returns key of token
        Arguments:
            obj (User): user being serialized
        Returns:
            token_key (str): key of token associated to user
        """
        req_user = self.context['request'].user
        return None if obj != req_user else obj.auth_token.key

    def create(self, validated_data):
        serializer = ProfileSerializer(data=validated_data.pop('profile'))
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(**validated_data)
        serializer.save(user=user)
        return user

    def update(self, instance, validated_data):
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(validated_data.get('password'))
        instance.save()

        # saving changes to profile model for the user
        try:
            profile = instance.profile
        except Profile.DoesNotExist:
            profile = None

        serializer = ProfileSerializer(profile, validated_data.get('profile', {}), partial=self.partial)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=instance)

        return instance
