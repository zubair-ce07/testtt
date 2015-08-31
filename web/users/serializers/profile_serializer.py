from rest_framework import serializers
from web.users.models import User
from web.users.serializers.address_serializer import AddressSerializer


class ProfileSerializer(serializers.ModelSerializer):

    address = AddressSerializer()
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'gender', 'born_on', 'address')

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address')
        address = instance.address
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
