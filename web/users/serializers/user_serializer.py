import re
from rest_framework import serializers
from web.users.models import User, Address
from web.users.serializers.address_serializer import AddressSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):

    address = AddressSerializer()

    class Meta:
        model = User
        fields = ('url', 'email', 'first_name', 'last_name', 'address', 'gender', 'born_on', 'password')

    # noinspection PyMethodMayBeStatic
    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError("Password is to short.")
        elif not re.search(r'[\W]+', password):
            raise serializers.ValidationError("Password must contain special character.")
        return password

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        user = User.objects.create(address=Address.objects.create(**address_data), **validated_data)
        return user

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address')
        address = instance.address
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.born_on = validated_data.get('born_on', instance.born_on)
        address.zip_code = address_data.get('zip_code', address.zip_code)
        address.street = address_data.get('street', address.street)
        address.route = address_data.get('route', address.route)
        address.city = address_data.get('city', address.city)
        address.state = address_data.get('state', address.state)
        address.country = address_data.get('country', address.country)
        address.save()
        instance.save()
        return instance
