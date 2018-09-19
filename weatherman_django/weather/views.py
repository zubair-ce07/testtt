from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Max, Min, Avg

from .serializers import YearlyWeatherSerializer, AvergaeMonthlyWeatherSerializer
from .models import Weather


class YearlyTemperature(APIView):
    serializer_class = YearlyWeatherSerializer

    def get_query_set(self, year):
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
        weather = self.get_query_set(year)
        if weather is None:
            return Response({"message": "Please enter a valid year."})
        if weather['higest_temperature'] or weather['lowest_temperature'] or weather['humidity']:
            serializer = YearlyWeatherSerializer(weather)
            return Response(serializer.data)
        else:
            return Response({"message": "sorry no record found for this year"})


class AverageTemperature(APIView):
    serializer_class = AvergaeMonthlyWeatherSerializer

    def get_query_set(self, year, month):
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
        weather = self.get_query_set(year, month)
        if weather is None:
            return Response({"message": "Please enter a valid year and month."})
        if weather['higest_average'] or weather['lowest_average'] or weather['average_humidity']:
            serializer = AvergaeMonthlyWeatherSerializer(weather)
            return Response(serializer.data)
        else:
            return Response({"message": "sorry no record found for this month and year"})
