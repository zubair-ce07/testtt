from rest_framework import serializers
from url_crawler.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
    serializes data for user model. and provide
    create and update methods for user.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'date_of_birth', 'photo', 'email', 'password')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        photo = validated_data.get('photo', None)
        if photo:
            instance.photo = photo

        instance.save()
        return instance
