import json
from datetime import date
from collections import OrderedDict

from django.utils.dateformat import DateFormat
from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import WeatherModel
from .serializers import WeatherSerializer


class WeatherViewSet(viewsets.ModelViewSet):
    '''
    API endpoint viewset for WeatherModel class
    '''
    queryset = WeatherModel.objects.all()
    serializer_class = WeatherSerializer


class WeatherSummaryView(APIView):
    '''
    gives summary of the weather data
    '''

    def get(self, request, format=None):
        '''
        Method to get summary data based on url parameters
        '''
        response_dict = {}
        response_dict['status'] = True,
        response_dict['error'] = '',
        params = request.query_params
        startdate = date.fromordinal(int(
            params['startdate'])) if 'startdate' in params else date(
                date.today().year, 1, 1)
        enddate = date.fromordinal(int(
            params['enddate'])) if 'enddate' in params else date.today()
        items = int(params['items']) if 'items' in params else 10

        the_status = status.HTTP_200_OK
        summary_dict = {}
        param_dict = OrderedDict([
            ('start_date', DateFormat(startdate).format('Y-m-d')),
            ('end_date', DateFormat(enddate).format('Y-m-d')),
            ('items', items),
        ])
        if items < 0:
            response_dict['status'] = False,
            response_dict['error'] = 'items should be greater than 0',
            the_status = status.HTTP_400_BAD_REQUEST
            return Response(response_dict, status=the_status)
        if items == 0:
            response_dict['status'] = False,
            response_dict['error'] = 'No Content',
            the_status = status.HTTP_204_NO_CONTENT
            return Response(response_dict, status=the_status)

        for key in ['temp', 'dew', 'humidity', 'sea_pressure', 'visibility']:
            max_key = 'max_' + key
            mean_key = 'mean_' + key
            min_key = 'min_' + key
            max_ = [getattr(instance, max_key) for instance in WeatherModel.objects.filter(
                    date__gte=startdate, date__lt=enddate).order_by(
                        '-' + max_key)[:items]]
            mean_list = [getattr(instance, mean_key)
                         for instance in WeatherModel.objects.all()[:items]]
            mean_ = sum(mean_list) / len(mean_list)

            min_ = [getattr(instance, min_key) for instance in WeatherModel.objects.filter(
                    date__gte=startdate, date__lte=enddate).order_by(min_key)[:items]]
            summary_dict[max_key] = max_
            summary_dict[mean_key] = mean_
            summary_dict[min_key] = min_

        response_dict['params'] = param_dict
        response_dict['summary'] = summary_dict
        return Response(response_dict, status=the_status)
