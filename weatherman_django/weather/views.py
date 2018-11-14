"""
this module contans the views of this django app
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Max, Min, Avg
from rest_framework.generics import ListAPIView

from .serializers import YearlyWeatherSerializer, AverageMonthlyWeatherSerializer, CitySerializer, \
    YearSerializer
from .models import Weather, City


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
    serializer_class = AverageMonthlyWeatherSerializer

    def get_query_set(self, year, month):
        """
        return queryset for particualr month and year
        :param year:
        :param month:
        :return:
        """
        try:
            if month:

                weather = Weather.objects.filter(
                    date__year=year,
                    date__month=month
                ).aggregate(
                    higest_average=Avg('temperature__max_value'),
                    lowest_average=Avg('temperature__min_value'),
                    average_humidity=Avg('humidity__mean_value')
                )
                return weather
            else:

                weather = Weather.objects.filter(
                    date__year=year,
                ).values(
                    'date__month'
                ).annotate(
                    higest_average=Avg('temperature__max_value'),
                    lowest_average=Avg('temperature__min_value'),
                    average_humidity=Avg('humidity__mean_value')
                )
                return weather

        except ValueError:
            return None

    def get(self, request, year, month=None):
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
        if isinstance(weather, dict):
            if weather['higest_average'] or weather['lowest_average'] \
                    or weather['average_humidity']:
                serializer = AverageMonthlyWeatherSerializer(weather)
                return Response(serializer.data)
            else:
                return Response({"message": "sorry no record found for this month and year"})
        elif len(weather):
            serializer = AverageMonthlyWeatherSerializer(weather, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "sorry no record found for this year"})


class GetAllCities(ListAPIView):
    """
    A class that returns all the cities present in the DB
    """
    serializer_class = CitySerializer
    queryset = City.objects.all()


class GetYearsOfCity(APIView):
    """
    it return the years for which temeprature record is present for a city
    """
    serializer_class = YearSerializer

    def get_query_set(self, city):
        """
        return weather data of a particualr city
        :param city:
        :return:
        """
        return Weather.objects.filter(city_id=city).values('date__year').order_by(
            'date__year').distinct()

    def get(self, request, city):
        years = self.get_query_set(city)

        serializer = YearSerializer(years, many=True)
        return Response(serializer.data)
