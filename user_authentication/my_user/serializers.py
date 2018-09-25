"""
this module contains the serializers for this django app
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    This is a serializer class for user registration
    """
    password1 = serializers.CharField(style={'input_type': 'password'})
    password2 = serializers.CharField(style={'input_type': 'password', 'label': "Password"})

    class Meta:
        """
        Meta class of UserRegisterSerializer
        """
        model = User
        fields = ['username', 'password1', 'password2']

    def validate(self, attrs):
        """
        this is override method, it validates the register form data
        :param attrs:
        :return:
        """
        username = attrs['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            password1 = attrs['password1']
            if not password1:
                raise serializers.ValidationError({'password1': "Password is required"})
            password2 = attrs['password2']
            if not password2:
                raise serializers.ValidationError({'password2': "Kindly repeat your password"})
            if password1 != password2:
                raise serializers.ValidationError(
                    {'password2': "The two password fields didn't match."})
            return attrs
        else:
            raise serializers.ValidationError({'username': "Username should be unique"})

    def create(self, validated_data):
        """
        this method creates a new user from verified data
        :param validated_data:
        :return:
        """
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password1'])
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    This is a serializer class for user login
    """

    def create(self, validated_data):
        """
        implement the abstract method
        :param validated_data:
        :return:
        """
        pass

    def update(self, instance, validated_data):
        """
        implement the abstract method
        :param instance:
        :param validated_data:
        :return:
        """
        pass

    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        """
        Meta class of UserLoginSerializer
        """
        fields = ['username', 'password']

    def validate(self, attrs):
        """
        it validates the login form data
        :param attrs:
        :return:
        """
        username = attrs['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({'username': "Please enter a valid username"})
        else:
            password = attrs['password']
            pwd_valid = check_password(password, user.password)
            if not pwd_valid:
                raise serializers.ValidationError(
                    {'password': "Incorrect Password."})
            return attrs


class UserEditSerializer(serializers.ModelSerializer):
    """
    This is a serializer class for user profile update
    """

    class Meta:
        """
        Meta class of UserEditSerializer
        """
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def validate(self, attrs):
        """
        it validates the Edit form's data
        :param attrs:
        :return:
        """
        username = attrs['username']
        if self.instance.username != username:
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                pass
            else:
                raise serializers.ValidationError({'username': "Please enter a valid username"})
        return attrs


class UserEditPasswordSerializer(serializers.Serializer):
    """
    This is a serializer class for user password update
    """

    def create(self, validated_data):
        """
        just have to implement this method of abstract class
        :param validated_data:
        :return:
        """
        pass

    password = serializers.CharField(style={'input_type': 'password'}, label="Old Password")
    password1 = serializers.CharField(style={'input_type': 'password'}, label="New Password")
    password2 = serializers.CharField(style={'input_type': 'password'}, label="Repeat Password")

    class Meta:
        """
        Meta class of UserEditPasswordSerializer
        """
        fields = ['password', 'password1', 'password2']

    def validate(self, attrs):
        """
        it validates the change password form's data
        :param attrs:
        :return:
        """
        password = attrs['password']

        pwd_valid = check_password(password, self.instance.password)

        if pwd_valid:
            password1 = attrs['password1']
            if not password1:
                raise serializers.ValidationError({'password1': "Password is required"})
            password2 = attrs['password2']
            if not password2:
                raise serializers.ValidationError({'password2': "Kindly repeat your password"})
            if password1 != password2:
                raise serializers.ValidationError(
                    {'password2': "The two password fields didn't match."})
            return attrs
        else:
            raise serializers.ValidationError({'password': "Please enter your correct Password"})

    def update(self, instance, validated_data):
        """
        updates the users password
        :param instance:
        :param validated_data:
        :return:
        """
        instance.set_password(validated_data['password1'])
        instance.save()
        return instance
