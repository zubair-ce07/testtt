from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password


class UserRegisterSerializer(serializers.ModelSerializer):
    """This is a serializer class for user registration"""
    password1 = serializers.CharField(style={'input_type': 'password'})
    password2 = serializers.CharField(style={'input_type': 'password', 'label': "Password"})

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def validate(self, data):
        username = data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            password1 = data['password1']
            if not password1:
                raise serializers.ValidationError({'password1': "Password is required"})
            password2 = data['password2']
            if not password2:
                raise serializers.ValidationError({'password2': "Kindly repeat your password"})
            if password1 != password2:
                raise serializers.ValidationError(
                    {'password2': "The two password fields didn't match."})
            return data
        else:
            raise serializers.ValidationError({'username': "Username should be unique"})

    def create(self, validated_data):
        return User.objects.create(username=validated_data['username'],
                                   password=validated_data['password1'])


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        fields = ['username', 'password']

    def validate(self, data):
        username = data['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({'username': "Please enter a valid username"})
        else:
            password = data['password']
            pwd_valid = check_password(password, user.password)
            if not pwd_valid:
                raise serializers.ValidationError(
                    {'password': "Incorrect Password."})
            return data


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def validate(self, data):
        username = data['username']
        if self.instance.username != username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                pass
            else:
                raise serializers.ValidationError({'username': "Please enter a valid username"})
        return data


class UserEditPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(style={'input_type': 'password'}, label="Old Password")
    password1 = serializers.CharField(style={'input_type': 'password'}, label="New Password")
    password2 = serializers.CharField(style={'input_type': 'password'}, label="Repeat Password")

    class Meta:
        fields = ['password', 'password1', 'password2']
        # fields = ['password']

    def validate(self, data):
        password = data['password']

        pwd_valid = check_password(password, self.instance.password)
        # pwd_valid= True
        if pwd_valid:
            password1 = data['password1']
            if not password1:
                raise serializers.ValidationError({'password1': "Password is required"})
            password2 = data['password2']
            if not password2:
                raise serializers.ValidationError({'password2': "Kindly repeat your password"})
            if password1 != password2:
                raise serializers.ValidationError(
                    {'password2': "The two password fields didn't match."})
            return data
        else:
            raise serializers.ValidationError({'password': "Please enter your correct Password"})

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password1'])
        instance.save()
        return instance
