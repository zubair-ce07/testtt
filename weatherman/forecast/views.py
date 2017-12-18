# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from forecast.core.weatherman import generate
from weatherman import settings


def index(request):
    return render(request, 'forecast/index.html', {})


class WeatherInfo(APIView):
    def get(self, request, format=None):
        report = generate(request.GET, settings.BASE_DIR + "/../weatherfiles")
        return Response(report)
