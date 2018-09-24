"""
this module contans the views of this django app
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Max, Min, Avg

from .serializers import YearlyWeatherSerializer, AvergaeMonthlyWeatherSerializer
from .models import Weather


class YearlyTemperature(APIView):
    """
    for getting yearly max, min temprature and max humidity of a given year
    """
    serializer_class = YearlyWeatherSerializer

    def get_query_set(self, year):
        """
        return a queryset for particular year
        :param year:
        :return:
        """
        try:
            weather = Weather.objects.filter(
                date__year=year
            ).values(
                'temperature__max_value',
                'temperature__min_value',
                'humidity__max_value',
            ).aggregate(
                higest_temperature=Max('temperature__max_value'),
                lowest_temperature=Min('temperature__min_value'),
                humidity=Max('humidity__max_value')
            )
            return weather
        except ValueError:
            return None

    def get(self, request, year):
        """
        to get yearly temprature of a year
        :param request:
        :param year:
        :return:
        """
        weather = self.get_query_set(year)
        if weather is None:
            return Response({"message": "Please enter a valid year."})
        if weather['higest_temperature'] or weather['lowest_temperature'] or weather['humidity']:
            serializer = YearlyWeatherSerializer(weather)
            return Response(serializer.data)
        else:
            return Response({"message": "sorry no record found for this year"})


class AverageTemperature(APIView):
    """
    to get average tempratures and humidity of a given month
    """
    serializer_class = AvergaeMonthlyWeatherSerializer

    def get_query_set(self, year, month):
        """
        return queryset for particualr month and year
        :param year:
        :param month:
        :return:
        """
        try:
            weather = Weather.objects.filter(
                date__year=year,
                date__month=month
            ).values(
                'temperature__max_value',
                'temperature__min_value',
                'humidity__mean_value',
            ).aggregate(
                higest_average=Avg('temperature__max_value'),
                lowest_average=Avg('temperature__min_value'),
                average_humidity=Avg('humidity__mean_value')
            )
            return weather
        except ValueError:
            return None

    def get(self, request, year, month):
        """
        to get the monthly temprature for a given month
        :param request:
        :param year:
        :param month:
        :return:
        """
        weather = self.get_query_set(year, month)
        if weather is None:
            return Response({"message": "Please enter a valid year and month."})
        if weather['higest_average'] or weather['lowest_average'] or weather['average_humidity']:
            serializer = AvergaeMonthlyWeatherSerializer(weather)
            return Response(serializer.data)
        else:
            return Response({"message": "sorry no record found for this month and year"})
