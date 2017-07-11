from rest_framework import serializers

from .models import WeatherModel


class WeatherSerializer(serializers.ModelSerializer):
    '''
    Simple model serializer for WeatherModel
    '''
    class Meta:
        model = WeatherModel
        fields = '__all__'
