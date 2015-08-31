import re
from rest_framework import serializers
from web.users.models import User, Address
from web.users.serializers.address_serializer import AddressSerializer
from web.constants import *


class UserSerializer(serializers.ModelSerializer):

    address = AddressSerializer()

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'address', 'gender', 'born_on', 'password')

    # noinspection PyMethodMayBeStatic
    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError(PASSWORD_IS_TOO_SHORT)
        elif not re.search(r'[\W]+', password):
            raise serializers.ValidationError(MUST_HAVE_A_SPECIAL_CHARACTER)
        return password

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        password = validated_data.pop('password')
        user = User.objects.create(address=Address.objects.create(**address_data), **validated_data)
        user.set_password(password)
        user.save()
        return user
