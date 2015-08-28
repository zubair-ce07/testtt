from rest_framework import serializers
from web.users.models import Address


class AddressSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Address
        fields = ('zip_code', 'street', 'route', 'city', 'state', 'country')