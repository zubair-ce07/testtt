from rest_framework import serializers

from .models import WeatherModel


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherModel
        fields = '__all__'
