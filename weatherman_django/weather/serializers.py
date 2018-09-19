from rest_framework import serializers
from .models import Weather


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = "__all__"


class YearlyWeatherSerializer(serializers.Serializer):
    higest_temperature = serializers.IntegerField()
    lowest_temperature = serializers.IntegerField()
    humidity = serializers.IntegerField()

    class Meta:
        fields = ['higest_temperature', 'lowest_temperature', 'humidity']


class AvergaeMonthlyWeatherSerializer(serializers.Serializer):
    higest_average = serializers.IntegerField()
    lowest_average = serializers.IntegerField()
    average_humidity = serializers.IntegerField()

    class Meta:
        fields = ['higest_average', 'lowest_average', 'average_humidity']
