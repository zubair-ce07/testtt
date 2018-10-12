"""
this module contains the serializers for this django app
"""
from rest_framework import serializers
from .models import Weather


class WeatherSerializer(serializers.ModelSerializer):
    """
    Serializer class for weather
    """

    class Meta:
        """
        Meta class for WeatherSerializer
        """
        model = Weather
        fields = "__all__"


class YearlyWeatherSerializer(serializers.Serializer):
    """
    serializer class for Yearly Weather
    """
    higest_temperature = serializers.IntegerField()
    lowest_temperature = serializers.IntegerField()
    humidity = serializers.IntegerField()

    class Meta:
        """
        Meta class for YearlyWeatherSerializer
        """
        fields = ['higest_temperature', 'lowest_temperature', 'humidity']


class AvergaeMonthlyWeatherSerializer(serializers.Serializer):
    """
    serializer class for Average Monthly Weather
    """
    higest_average = serializers.IntegerField()
    lowest_average = serializers.IntegerField()
    average_humidity = serializers.IntegerField()

    class Meta:
        """
        Meta class for AvergaeMonthlyWeatherSerializer
        """
        fields = ['higest_average', 'lowest_average', 'average_humidity']
