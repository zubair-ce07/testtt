from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    serializes data for user model. Along with user details provides
    with user's own token.
    """
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'date_of_birth', 'photo', 'email', 'password', 'token',)

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
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.email = validated_data.get('email', instance.email)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        instance.save()
        return instance
