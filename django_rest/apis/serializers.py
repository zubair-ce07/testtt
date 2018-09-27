from rest_framework import serializers

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',
                  'username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
