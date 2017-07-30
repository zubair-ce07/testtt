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
        serializer = AddressSerializer(instance.address, validated_data.get('address', {}), partial=self.partial)
        if serializer.is_valid():
            serializer.save()

        return instance


class UserSerializer(serializers.ModelSerializer):
    """
    serializes data for user model. Along with user details provides
    with user's own token.
    """
    profile = ProfileSerializer()
    password = serializers.CharField(write_only=True)
    token = serializers.ReadOnlyField(source='auth_token.key')

    class Meta:
        model = User
        fields = ('id', 'phone', 'email', 'profile', 'password', 'token',)

    def to_representation(self, instance):
        # this makes sure that user can only see his own token.
        representation = super(UserSerializer, self).to_representation(instance)
        if instance != self.context['request'].user:
            representation.pop('token')
        return representation

    def create(self, validated_data):
        profile = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        address = Address.objects.create(**profile.pop('address'))
        designation, created = Designation.objects.get_or_create(**profile.pop('designation'))
        profile = Profile.objects.create(user=user, address=address, designation=designation, **profile)
        return user

    def update(self, instance, validated_data):
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(validated_data.get('password'))
        instance.save()

        # saving changes to profile model for the user
        serializer = ProfileSerializer(instance.profile, validated_data.get('profile', {}), partial=self.partial)
        if serializer.is_valid():
            serializer.save()

        return instance
